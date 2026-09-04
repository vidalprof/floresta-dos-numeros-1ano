# 🔎 Pesquisa: direito-de-desligar-usuario-comum-windows

> Busca: `"Shut down the system" user right assignment default Users group Windows 10 workstation standard user can run shutdown.exe without administrator access denied 5 group policy remove`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## cant access shutdown and restart Users under GPO - Microsoft Q&A

`https://learn.microsoft.com/en-us/answers/questions/1104624/cant-access-shutdown-and-restart-users-under-gpo`

cant access shutdown and restart Users under GPO - Microsoft Q&A

cant access shutdown and restart Users under GPO

All users i created it, doesn't have and can't access shutdown and restart, cause it disabled and i want to activate it.

Windows for business | Windows Client for IT Pros | User experience | Other

Windows for business | Windows Client for IT Pros | User experience | Other

Based on my research and test, I find the group policy settings below may control the Shut Down and Restart function.

If I configured User Configuration -> Administrative Templates -> Start Menu and Taskbar -> Remove and prevent access to the Shut Down, Restart, Sleep, and Hibernate commands" to Enabled (By default it is Not Configured).

Computer Configuration -> Administrative Templates -> Start Menu and Taskbar -> Remove and prevent access to the Shut Down, Restart, Sleep, and Hibernate commands" to Enabled (By default it is Not Configured).

I will not see Shut Down and Restart options on the Start menu.

If I configured Computer Configuration -> Windows Setting -> Security Setting -> Local Policies -> User Right Assignment ->Shut down the system -> If I remove the Users group (By default, there are three groups: Administrators, Back Operators and Users).

I will not see Shut Down and Restart options on the Start menu.

You can check if the Users group is included in Shut down the system.

Tip: If your machines and users are in one domain, you had to check both local group policy and domain GPO.

If your machines and users are in one workgroup, you only need to check local group policy.

============================================

---

## 2.2.38 Ensure 'Shut down the system' is set to 'Administrators, Users' (Level 1)

`https://www.syxsense.com/syxsense-securityarticles/cis_benchmarks/syx-1033-15601.html`

2.2.38 Ensure 'Shut down the system' is set to 'Administrators, Users' (Level 1)

CIS Microsoft Windows 10 Enterprise Benchmark v4.0.0

ð 2 Local Policies | 2.2 User Rights Assignment

2.2.38 Ensure 'Shut down the system' is set to 'Administrators, Users' (Level 1)

2.2.38 'User Rights Assignment: Shut down the system' recommended state is 'Administrators, Users'

This policy setting determines which users who are logged on locally to the computers in your environment can shut down the operating system with the Shut Down command. Misuse of this user right can result in a denial of service condition.

The ability to shut down a workstation should be available generally to Administrators and authorized users of that workstation, but not permitted for guests or unauthorized users - in order to prevent a Denial of Service attack.

To configure the policy as recommended, follow the steps below:

This vulnerability can be automatically fixed within the console.

Press Windows+R keys and type 'gpedit.msc' and press OK;

Navigate to: Computer Configuration\Windows Settings\Security Settings\Local Policies\User Rights Assignment

On the right pane double click the 'Shut down the system' setting

Ensure the policy is set to Administrators, Users

If the policy is not configured as recommended, click the 'Add User or Group' button to add the required group (Click 'Add User or Group' > 'Advanced' > 'Find now' and choose it from the list). Ensure

the recommended groups are included. You can remove any unnecessary groups by selecting them and clicking the 'Remove' button.

Before adding specific groups, ensure that you've added 'Object types' to include groups in your search:

In the 'Select Users, Computers, or Groups' window click on the 'Object Types' button.

Check the box next to 'Groups' to include groups in your search

CIS BenchmarksÂ® List/Download Benchmarks

---

## ⚠️ Paginas que NAO deram texto

- `https://www.anavem.com/en/tools/group-policy-reference/shut-down-the-system` — HTTP 404
- `https://www.techcrafters.com/portal/en/kb/articles/how-to-allow-or-prevent-non-admin-users-from-rebooting-or-shutting-down-windows` — bloqueada ou vazia
- `https://www.ultimatewindowssecurity.com/wiki/page.aspx?spid=ShutdownSystem` — bloqueada ou vazia
