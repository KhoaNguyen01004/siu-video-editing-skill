# Bring CapCut's main window to the front, maximized (it starts minimized when launched by automation).
Start-Sleep -Seconds 6
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices;
public class CapWin {
  public delegate bool EP(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EP f, IntPtr l);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint p);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern void keybd_event(byte v, byte s, uint f, UIntPtr e);
  public static IntPtr Find(uint[] pids) { IntPtr r = IntPtr.Zero; EnumWindows((h,l)=>{ uint p; GetWindowThreadProcessId(h, out p); var s=new StringBuilder(256); GetWindowText(h,s,256); if (Array.IndexOf(pids,p)>=0 && IsWindowVisible(h) && s.ToString()=="CapCut"){ r=h; return false;} return true;}, IntPtr.Zero); return r; }
}
"@
$h = [CapWin]::Find([uint32[]](Get-Process CapCut | ForEach-Object Id))
[CapWin]::ShowWindow($h, 9) | Out-Null; [CapWin]::keybd_event(0x12,0,0,[UIntPtr]::Zero); [CapWin]::keybd_event(0x12,0,2,[UIntPtr]::Zero)
[CapWin]::SetForegroundWindow($h) | Out-Null; [CapWin]::ShowWindow($h, 3) | Out-Null; "hwnd $h"

# If a Pro / trial popup ignores clicks and Escape, close it like its X button (WM_CLOSE). List CapCut's visible windows
# first; the popup is the small one titled "CapCut":
#   $pids = [uint32[]](Get-Process CapCut | ForEach-Object Id)
#   (enumerate with EnumWindows + GetWindowRect, as above) -> [W]::SendMessage($popupHwnd, 0x0010, 0, 0)
# Never click Purchase / Try / Join Pro.
