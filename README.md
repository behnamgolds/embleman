# embleman

### A set of emblem actions built on top of a previous project [numblems](https://github.com/behnamgolds/xfce-thunar-numblems)
 
### There is also a [Go implementation](https://github.com/behnamgolds/embleman-go) if you are interested.
 
![1](https://github.com/behnamgolds/embleman/assets/29102609/12e499ba-794d-47f6-b3df-958e8b431973)

I just wanted to add some actions to my thunar custom actions ,
so that I could mark some files/directories with a number or 
some other emblems and easily increase or decrease the number .

This was intended to be used as thunar custom action, but it
could also be used on its own like this :

```bash
python embleman.py < --increse | --decrease | --clock | --check > <file-or-directory-path>
```
or
```bash
./embleman.py --help
```
But you have to refresh(F5) your thunar window manually.
If used as thunar custom action it will automatically send
the F5 key to the active window(aka thunar)

You could also use it in other scripts and just run something
like the following to send F5 to the active window :
```bash
xdotool key F5
```

I used some svg emblems and put it into my icons directory here :
```
~/.icons/Papirus-Dark/symbolic/emblems/
```
There are 19 [1..19] svgs since that is what I needed .
The script will clear the emblem if the number goes out of range .
I included them in the emblems/ directory in this repo .
Also the source is mentioned there in emblems/source.txt .
"Papirus-Dark" is the name of the theme I use, you should change
it to your theme name and make a symbolic link to this directory
in your "your-theme-name" directory if you want these emblems to
be visible in other themes .

then run this to make thunar read the new emblems :
```bash
thunar -q
```

My embleman script is located here :
```
~/bin/non-interactive/
```
Adding the action to thunar is straightforward from :
```
Thunar > Edit > Configure Custom Actions
```

![2](https://github.com/behnamgolds/embleman/assets/29102609/cfaea98a-4d41-4246-a504-b6682d54d6ce)


The changes will be saved here :
```
~/.config/Thunar/uca.xml
```
The changes related to embleman for my config will be saved like this :
```xml
</actions>
<action>
	<icon>mx-cleanup</icon>
	<name>Clear</name>
	<submenu>Emblem</submenu>
	<unique-id>1702979225176410-1</unique-id>
	<command>/home/behnam/bin/non-interactive/embleman.py --clear  %F</command>
	<description>Clear Emblems</description>
	<range></range>
	<patterns>*</patterns>
	<directories/>
	<audio-files/>
	<image-files/>
	<other-files/>
	<text-files/>
	<video-files/>
</action>
<action>
	<icon>vcs-normal</icon>
	<name>Check</name>
	<submenu>Emblem</submenu>
	<unique-id>1702646536255992-1</unique-id>
	<command>/home/behnam/bin/non-interactive/embleman.py --check  %f</command>
	<description>Add a check mark  to item</description>
	<range>1</range>
	<patterns>*</patterns>
	<directories/>
	<audio-files/>
	<image-files/>
	<other-files/>
	<text-files/>
	<video-files/>
</action>
<action>
	<icon>emblem-urgent</icon>
	<name>Clock</name>
	<submenu>Emblem</submenu>
	<unique-id>1706032898158192-1</unique-id>
	<command>/home/behnam/bin/non-interactive/embleman.py --clock  %f</command>
	<description>Add a clock mark to item</description>
	<range>1</range>
	<patterns>*</patterns>
	<directories/>
	<audio-files/>
	<image-files/>
	<other-files/>
	<text-files/>
	<video-files/>
</action>
<action>
	<icon>list-add</icon>
	<name>Inc Num</name>
	<submenu>Emblem</submenu>
	<unique-id>1717335346720586-1</unique-id>
	<command>/home/behnam/bin/non-interactive/embleman.py --increase %f</command>
	<description>Increase Number Emblem</description>
	<range>*</range>
	<patterns>*</patterns>
	<directories/>
	<audio-files/>
	<image-files/>
	<other-files/>
	<text-files/>
	<video-files/>
</action>
<action>
	<icon>list-remove</icon>
	<name>Dec Num</name>
	<submenu>Emblem</submenu>
	<unique-id>1717335485659165-2</unique-id>
	<command>/home/behnam/bin/non-interactive/embleman.py --decrease %f</command>
	<description>Decrease Number Emblem</description>
	<range>*</range>
	<patterns>*</patterns>
	<directories/>
	<audio-files/>
	<image-files/>
	<other-files/>
	<text-files/>
	<video-files/>
</action>
</actions>
```



