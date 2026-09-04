# 🔎 Pesquisa: desligar-pcs-sala-sem-admin

> Busca: `shut down all classroom computers from teacher web panel domain no admin rights Veyon power off students shutdown privilege standard user remote shutdown school lab`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## Troubleshooting — Veyon 4.10.4 documentation

`https://docs.veyon.io/en/latest/admin/troubleshooting.html`

Troubleshooting — Veyon 4.10.4 documentation

If you encounter interaction or connection problems between master and client computers you should always ensure that an identical Veyon configuration is used on all computers. To avoid problems in general it’s recommended to automate the configuration transfer during

instead of importing the configuration manually using the Veyon Configurator. The configuration must also be transferred to all affected computers each time a change is made during troubleshooting.

There are multiple causes which can prevent access to a computer using Veyon Master.

First of all the general network connectivity of the computer should be checked. Use the utility

(which is usually included with every operating system) to diagnose connectivity problems.

If the computer can be pinged you should verify that the Veyon Service is running correctly. Open the Veyon Configurator and open the configuration page

the status of the service should be displayed with status

. Otherwise the service can be started using the button

. If this is not successful you should try reinstalling Veyon. If a new installation does not help you can check the log files of the Veyon Service as well as the logging messages of the operating system for error messages and possible causes. Additionally you can find more hints or settings in the service management of your operating system.

If the service is running you have to ensure that it is listening for incoming connections on the correct network port. You can verify that on the local computer using

Besides general program output the character string

must be displayed. If the output does not contain these characters you should check the

, especially the Veyon server port number. You should try to reset them to their default values.

Next the same access has to be possible from a different computer in the network. The utility

can be used again for the diagnosis. The program argument

has to be replaced with the name or IP address of the corresponding computer. If the access fails please ensure that the option

should be disabled initially as the service otherwise might listen on

only. This can happen if the external access would be denied because of currently matching rules. If both settings are correct the output of

has to indicate that the service is not (only) listening on

If the port access from remote computers still fails usually a firewall prevents the access and has to be reconfigured accordingly. On Linux this concerns settings of

etc. Consult the corresponding manuals of the used software. On Windows Veyon automatically configures the integrated Windows firewall if the option

). If a 3rd party firewall solution is used it must be configured to allow external access to TCP ports 11100 (Veyon server port) and 11400 (demo server).

Another cause of the error can be wrong or insufficient

on both computers. As soon as the authentication test is successful on the local computer external access will also work.

is used the key files on master and client computers must match exactly. On client computers the public key file must have exactly the same content

as on the master computer. If the access still fails the access permissions to the key files may be wrong. The Veyon Service needs to have read permissions on the

while the user of Veyon Master has to be able to read the

of the key files should be deleted on all computers and a new key pair generated on the master computer. The public key must then be imported again on all client computers.

An incorrect configuration of computer access control can also lead to computers being inaccessible. Initially it’s recommended to disable

completely using the Veyon Configurator. This allows you to determine which method of computer access control may be configured incorrectly.

authorized user groups for computer access

are used you should check whether the list of authorized user groups is complete and whether the accessing user is a member of one of these user groups.

can also cause problems with accessing computers. It is necessary to always specify at least one rule to allow access under certain conditions. If this is ensured, a temporary test rule can be inserted at the end of the list for further debugging. This rule should be configured so that the option

Always process rule and ignore conditions

is selected. This rule can then be moved up in the rule list step by step until the test returns the desired positive results and the access works. The access rule located directly below the test rule is then the cause for the access denial and can be examined more closely and corrected accordingly. Don’t forget to remove the test rule afterwards to prevent unauthorized access.

It has been reported by some users that an installed anti-virus software caused problems with Veyon, especially regarding the Veyon Service. As part of the troubleshooting process you should temporarily disable the anti-virus software in order to figure out whether the anti-virus software is the cause of error. If so, try to add an exception for the Veyon Service after enabling the anti-virus software again. Alternatively contact the vendor of your anti-virus software for further assistance.

, Veyon requires the operating system to reliably perform user authentications on all remote computers. Especially in AD/Kerberos-based environments, authentication may not work reliably when the system clock is not synchronized with the domain controller or authentication server and differs significantly. Therefore make sure time synchronization is configured and working properly if you encounter sporadic connectivity problems when using Veyon.

After updating to a new version of Veyon it may happen in rare cases that some configuration keys are inconsistent and need to be recreated. This can result in settings not being saved or reloaded correctly, such as the builtin location and computer information. In this case the

Locations and computers from LDAP directory are not displayed in Veyon Master

all options for fine-tuning the behavior are set to their default values

Selecting current location automatically doesn’t work

option automatically selecting the current location

is activated, but has no effect when starting Veyon Master, you should first make sure that the master computer is also listed as a computer for the respective room in the

If the problem persists although all entries in the network object directory are correct, there is usually a problem with the DNS configuration in the network. Make sure that computer names can be resolved to IP addresses and reverse lookups of IP addresses return the corresponding computer names. On most operating systems, the DNS diagnostic tool

is available for this purpose. Calling the program with the local computer name as an argument must return a valid IP address. A second call with the determined IP address must again return the computer name.

If the function does not work as desired despite correct DNS setup, in the second step the

). After restarting Veyon Master, you can search the log file

for further error causes. The lines with the messages

indicate which host names and IP addresses were used to determine the location and which locations were eventually determined on the basis of these information.

Screen lock can be bypassed via Ctrl+Alt+Del

To completely block all keystrokes and keyboard shortcuts in screen lock mode, you must restart your computer after installing Veyon on Windows. Without a restart, the Veyon-specific driver for input devices is not yet active and keystrokes cannot be intercepted.

In demo mode, only a black screen or window with a blue loading spinner is displayed on client computers

the user of Veyon Master has access to its own computer (i.e. the local Veyon Service). When using the

make sure the public key is deployed to both student

there’s no rule preventing the teacher from accessing its own computer, e.g. a rule prohibiting access to a computer if a teacher is logged on. In this case you should create a rule with the condition

enabled as far up the list of rules as possible. Otherwise the demo server is unable to access the teacher computer’s screen content and distribute it to the client computers.

the demo server port is set to its default value

the firewall exception is enabled on the master computer or a third party firewall is configured to allow incoming connections to TCP port

Veyon Server crashes with XIO or XCB errors on Linux

There are known issues with specific KDE and Qt versions on Linux causing the Veyon Server to crash. This affects several other VNC server implementations as well. If you’re affected by such crashes consider upgrading KDE/Qt. As a last resort you can disable the X Damage extension in the VNC server configuration. This will however decrease overall performance and increase the CPU load.

Some features such as starting apps or opening websites do not work

It has been reported that problems arise if the username and the computer name are identical. When logging in a user called

, some features will fail to start when the user session is being controlled via Veyon Master.

---

## Help & Troubleshooting | Veyon Community Forum

`https://veyon.nodebb.com/category/4/help-troubleshooting`

Help & Troubleshooting | Veyon Community Forum

You're facing difficulties with setting up Veyon? Ask away!

Hi Folks. I've just updated from 4.8.3 to 4.11.2 and have started getting the delays connecting to the client. I've managed to download 4.11.1.0 to see if there is any difference one version back. Has anyone else noticed this?

Update. Still the same and I've gone back a couple of versions. I'm wonder if it is our networ as the teacher said he never had this issue last academic year

Mouse and keyboard Interception drivers blocked by App control for Business in intune, since Windows 11 July 2026 updates

When I double-click on a student post from Veyon Master, the application closes.

Veyon CLI: limit administrator privileges

Veyon 4.10.3: Automatic reboot and logout loop at login screen on Master/Teacher PC

@tobydox If necessary, we will also use the debug mode. Thank you.

Veyon 4.10.3: Loop di riavvio automatico e disconnessione alla schermata di login sul PC Master/Docente

Starting with Veyon 4.10.3 there are dedicated packages for Fedora 44.

Hi. Just use the IntuneWinAppUtil.exe. The packaging tool converts application installation files into the .intunewin format.

Logon error with local user SSPLogonUser false 1385

I'm getting the same error only with some users in our AD domain. Technicians with elevated rights in AD are able to authenticate to the Master program, but other users, like Teachers cannot. All the LDAP setup works fine after that, but the initial authentication fails with:

2026-05-12T12:51:01.160: [ERR] AcceptSecurityContext failed with 8009030C

2026-05-12T12:51:01.161: [DEBUG] WindowsUserFunctions::authenticate(): SSPLogonUser() false 1385

ldap authorized user groups to restrict access not working in 4.10.2

I may be dealing with a similar problem on my side (version 4.10.1). I found out that access control is basically not used at all when I use authentication keys. I have an access group assigned to the authentication key, and if the user is in that group, it works even if the user is restricted through access control.

At the same time, I have another issue: when I add another group (nested group) into the group assigned to the key, the user is not recognized.

[BUG?] new 4.10.2 can't start website, transfer file, nor start application

Problems with LDAP authentication on out-of-domain PCs

Having trouble to get Key on student PC with Intune installation

Can't logon Veyon Master from Entra ID enrolled computer

How can I keep the Veyon service working on the classroom PC's?

Looks like your connection to Veyon Community Forum was lost, please wait while we try to reconnect.

---

## Access control rules — Veyon 4.10.4 documentation

`https://docs.veyon.io/en/latest/admin/access-control-rules.html`

Access control rules — Veyon 4.10.4 documentation

Access control rules can be used to provide detailed control over which users can access specific computers under specific circumstances. In the following, the term

When a user attempts to access a computer, the defined access control rules are processed one after another until all conditions of a rule apply. As soon as all activated conditions of a rule apply, no further rules are processed and the stored action is executed (exception: rule is disabled).

The rules can be configured through the Veyon Configurator on the configuration page

. The rules list is empty by default. In this case, all access attempts are denied since there is no rule that explicitly allows access. This means that at least one rule must be defined that allows access under certain conditions.

a dialog opens which allows the creation of a new rule. Existing rules can be opened or edited by double-clicking them or by clicking the button with the pen symbol.

A rule basically consists of general settings, conditions and an action that is executed when all conditions apply. The dialog is divided into three sections. The meanings of the individual options in the various dialog sections are explained below.

A name for the rule should be defined in input field

first. The name is later used to identify the rule and is displayed in the rules list. For documentation purposes an optional description can be added to the

Always process rule and ignore conditions

causes the conditions set below not to be examined for rule processing and the set action is always executed. This particularly useful for fallback rules at the bottom of the rules list, where you can specify that the logged on user is asked for permission if no other rules apply.

option to determine that all activated conditions are inverted before evaluation, meaning that activated conditions must not apply. For example, if the condition

is activated, the rule only applies if one or more users are logged on. If a condition is configured so that a user must be a member of a specific group, the rule only applies, if the said user is

For a rule to be processed, one or more conditions must apply.

You can use this condition to specify that either the accessing or the locally logged in user must be a member of a specific group. The desired group can be selected. If no or only wrong groups are selectable, the

may have to be adjusted. Alternatively, a regular expression can be entered to control access from or to certain groups whose names match a certain pattern, e.g.

With this condition you can define that either the accessing or the local computer has to be located at a specific location. The desired location can be selected. If no or only wrong locations are selectable the

has to be adjusted. Alternatively, a regular expression can be entered to control access from or to multiple locations whose names match a certain pattern.

Accessing computer and local computer are at the same location

You can use this condition to specify that the accessing computer and the local computer must be in the same location. This can be used, for example, to prevent teachers from accessing computers outside their own classroom.

If this condition is enabled, the rule applies only if the accessing computer is the local computer. This ensures for example that teachers can access the local Veyon Service. This access is necessary for the Veyon Master to execute specific functions via the Veyon Service (e.g. the server for demo mode).

Accessing user has one or more groups in common with local (logged on) user

You can use this condition to specify that the accessing and the local user have to be members of at least one common group, for example a user group for a class or a seminar.

you can also allow a user to access his own sessions. This condition must be activated for this purpose.

Accessing computer and local computer are at the same location

an extended ruleset can be created allowing access to computer at other locations under certain conditions. This includes the possibility to access a computer if the accessing user is already connected. For example, if the teacher logs on to a teacher computer in room A and B simultaneously and displays the computers of room B displayed in Veyon Master, the computers in room B have a connection from the teacher. Then the teacher can also access room B from Veyon Master in room A if this condition is activated with an allow action.

This condition determines how a computer can be accessed when no user is logged on. For easier computer administration, it can be helpful to always be able to access a computer when no user is logged on.

If this condition is activated, the rule takes effect if there is already at least one connection to the local Veyon Service. This can be used, for example, to prevent parallel access to a computer.

If all the enabled conditions of a rule apply, a specific action is performed with respect to computer access. You can define this action in section

Access to a computer is allowed and further rules are not processed. If there is a rule in the rules list below that would deny access, access is still allowed. There must be at least one rule with this action.

Access to a computer is denied and further rules are not processed. If there is a rule in the rules list below that would allow access, access is still denied.

This action displays a dialog on the computer that allows the logged-in user to choose whether to allow or deny access. No further rules are processed regardless of the user’s decision.

This action makes the rule being ignore. Access control will be continued by processing the next rule. This option can be used to create an inactive dummy entry to visually subdivide the rules list.

button the rule and the changes made are accepted and the dialog is closed.

The defined access control rules are processed one after the other in the order of the list. The action of the first matching rule is executed, even if subsequent rules would also apply and lead to a different action.

All rules can be reordered via the buttons with the arrow symbols. Rules that should fundamentally prevent or allow access based on certain criteria should be placed as high up as possible. Rules to cover special cases can follow below. Rules for the implementation of fallback behaviour should be at the bottom.

If more than one condition is activated in a rule,

condition must apply for the rule to be applied (logical AND). If only one of several rules should apply (logical OR), several access control rules must be defined.

With basic knowledge of Boolean algebra, the option

can be used as negation operator in conjunction with inverted actions to model extended scenarios. For example, if a user must be a member of two specific groups to allow access to a computer, two separate rules can be created that deny access, if the user is

If there is no matching access control rule so that all activated conditions apply, access is denied and the connection is closed. This prevents an attacker from being accidentally allowed access due to an incomplete ruleset.

the configured ruleset can be checked with various scenarios using the

button. In the test dialog you can enter the parameters to simulate a scenario. With the button

the rules are processed with the given parameters and a message with the test result is displayed.

---

## Deploying Veyon as a Classroom Manager on RONIN

`https://blog.ronin.cloud/veyon-classroom-manager/`

Deploying Veyon as a Classroom Manager on RONIN

) is an open-source classroom management tool that lets you:

Lock keyboards and mice (when things get chaotic)

And the best part? It works beautifully in RONIN cloud lab environments!

In this guide, we’ll walk through how to install and configure Veyon for a teacher and student setup in RONIN.

A Windows machine with DCV installed (via

A Windows Machine with DCV installed (via

If you wish to manage student machines across multiple RONIN projects, the default security group rules will need to be configured by a RONIN Administrator in the AWS console to allow access on ports

Open the Veyon Installer and ensure the Veyon Master component is selected for install and deselect the Interception Driver (it is not recommended for remote desktop environments).

Run the Veyon Configurator at the end of the installation

Generate authentication keys by clicking on Authentication keys > Create Key Pair. Name the key pair something easy to remember like "Classroom" or the name of your particular class or group of students that you will be monitoring. This creates:

Select the public key and click "Export key" and save it somewhere you can easily find again as you will be importing this key on the student machines in the next section.

In the Veyon Configurator, click on General and under "Authentication" make sure "Key File Authentication" is selected:

Then, ensure "Network object directory" is set to "Builtin":

Now click on Service and make sure the Session Mode is set to "Active Session Mode":

Feel free to explore and adjust any other settings you wish under "Master" and "File Transfer". If using File Transfer functionality we recommend creating an obvious top level folder like

Click Apply at the bottom of the window and allow Veyon to restart

Open the Veyon Installer and ensure only the Veyon Service component is selected for install (deselect the other options since these are not required for student machines)

Run the Veyon Configurator at the end of the installation

On the Teacher machine, open the public key you exported earlier with Notepad and copy the contents

Back on the Student machine, open notepad and paste the contents of the public key that you copied to your clipboard from the Teacher machine

In the Veyon Configurator go to Authentication keys and click Import Key. Select the

file you saved - it should import successfully:

In the Veyon Configurator, click on General and under "Authentication" make sure "Key File Authentication" is selected:

Then, ensure "Network object directory" is set to "Builtin":

Now click on Service and make sure the Session Mode is set to "Active Session Mode":

Feel free to explore and adjust any other settings you wish under "Master" and "File Transfer". If using File Transfer functionality we recommend creating an obvious top level folder like

Click Apply at the bottom of the window and allow Veyon to restart

Once you have tested the connection (see next section) you can then install any other software, files etc that your students need and then prepare the machine for packaging to disperse to other students by following the steps in this blog post:

Preparing a Customized Windows Environment for Sharing

Want to share your custom Windows environment with other users but require them to set their own Administrator password? Find out how in this blog post!

Once your student package is created, you can then use it as a template to launch as many student machines as required and you will be able to manage them all from your Teacher machine.

On the teacher machine, open Veyon Master

Enter the RONIN machine address for the student machine e.g.

You should be able to remotely view the students screen:

Open the Veyon Configurator and click on Locations and Computers - in this window you can create your own "Classroom lists" of student machines

Make the Configurator full screen so that you can see all of the required columns properly

Scroll to the bottom to add a new "Location" (e.g. a class or group of students)

Then, with your new Location selected, scroll to the bottom again to add a student machine - the student's name can be placed in the Name column while the RONIN machine address e.g.

needs to be placed in the Host address/IP column.

Repeat this with as many student machines and classes as necessary

Click Apply at the bottom and then allow Veyon to restart

Your list of Locations/Classrooms and respective student machines should then appear in the Veyon Master tool under "Locations & Computers" in the bottom left:

Veyon has a variety of other options for interacting with the student machines including:

– Displays live thumbnail views of all student screens in near real time so teachers can monitor classroom activity at a glance.

– Allows the teacher to open any student computer in full-screen mode for closer observation.

– Enables the teacher to control a student’s mouse and keyboard to provide direct assistance or guidance.

– Broadcasts the teacher’s screen to selected or all student computers for live demonstrations.

– Temporarily disables student keyboard and mouse input while optionally displaying a custom message.

– Sends instant pop-up notifications or instructions to selected student machines.

– Captures and stores screenshots of student screens for documentation or review.

– Allows the teacher to log off, reboot, shut down, or wake student computers remotely.

– Transfers files between the teacher and student machines when enabled.

– Filters and organises student computers by name, user, or status to simplify classroom management.

Veyon is a powerful classroom management tool that is especially suited to cloud-hosted labs like those you can build with RONIN. It’s open source, cross-platform, and rich in features that help teachers maintain engagement and provide remote support. With a little upfront configuration you can create reproducible, scalable student environments fully manageable from a central teacher console.

---

## ⚠️ Paginas que NAO deram texto

- `https://www.scribd.com/document/548100345/veyon-admin-manual-en-4-6-0` — bloqueada ou vazia
- `https://www.scribd.com/document/448520434/veyon-admin-manual-en-4-2-5` — bloqueada ou vazia
