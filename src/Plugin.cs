using BepInEx;
using HarmonyLib;

namespace CarturFollowCommand
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    public class Plugin : BaseUnityPlugin
    {
        public const string PluginGuid = "com.jekkle.valheim.carturfollowcommand";
        public const string PluginName = "Cartur's Follow Command";
        public const string PluginVersion = "1.0.0";

        private void Awake()
        {
            Harmony.CreateAndPatchAll(typeof(Plugin).Assembly, PluginGuid);
            Logger.LogInfo($"{PluginName} {PluginVersion} loaded - Tameable.m_commandable forced true.");
        }
    }

    // Root cause: follow/stay is not a wolf feature, it is a Tameable feature that only wolves
    // and lox have switched on. The entire mechanism already ships in the base game -
    //
    //   Tameable.Interact  -> if (m_commandable) Command(user)
    //   Tameable.Command   -> InvokeRPC("Command")
    //   Tameable.RPC_Command -> MonsterAI.SetFollowTarget(player) / SetFollowTarget(null)+SetPatrolPoint()
    //                           and persists the owner name in ZDOVars.s_follow
    //   Tameable.UpdateSavedFollowTarget -> re-issues Command() on world load so it survives relogs
    //   MonsterAI.UpdateAI -> if (m_follow) Follow(m_follow, dt)   // no species check anywhere
    //
    // - and the single thing gating it is the m_commandable bool, which is set per-prefab in the
    // Unity asset and is false on boar, chicken, hen, asksvin and the rest. So there is nothing to
    // implement: flip the flag after Awake has read the prefab value, and the vanilla path handles
    // the button press, the toggle, the "$hud_tamefollow" / "$hud_tamestay" message, the networking
    // and the save. RPC_Command already null-checks m_monsterAI, so a Tameable without an AI
    // (saddle-only cases) stays a no-op rather than throwing.
    //
    // The button is the existing Use key (E by default) on the tamed animal, exactly as with a
    // wolf. No new keybind - a second one would just be a worse duplicate of the one players
    // already know.
    [HarmonyPatch(typeof(Tameable), "Awake")]
    public static class Patch_TameableAwake
    {
        static void Postfix(Tameable __instance)
        {
            __instance.m_commandable = true;
        }
    }
}
