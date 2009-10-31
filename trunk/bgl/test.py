import bgl
bgl=bgl.BGLFile("D:\\bgl-reverse\\local\\Babylon_English_Chinese_S_.bgl")
gls=bgl.toGlossary()
fout=open("D:\\bgl-reverse\\local\\enchs.txt","w",encoding='utf-8')
for entry in gls.entry_list:
	b=fout.write(entry.term)
	b=fout.write("\n")
	b=fout.write(entry.definition)
	b=fout.write("\n")
	b=fout.write(str(entry.attributes))
	b=fout.write("\n")
	b=fout.write(str(entry.alternatives))
	b=fout.write("\n\n")
fout.close()
