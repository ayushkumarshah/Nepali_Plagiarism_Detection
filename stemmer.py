class Stemmer:
    #Initialize
    suf_sub_rule,suffix_del,suffix_exist, suffix_look_posi, suffix_look_char, suffix_desc, \
    suffix_ins ,suffix_ins_posi, suffix_morph, suffix_type, suffix_ign, dub_suffix ,dub_suffix_morph,\
    dub_suffix_desc, pre_sub_rule, prefix_del, prefix_desc, prefix_ins, prefix_morph, prefix_type,\
    ht_root, ht_root_pos, suffix_ht, alt_root, ht_suffix, prefix_tm, ht_prefix=dict(),dict(),dict(),\
    dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),\
    dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict()
    parsetwo = 0
    sdes,smorph, subsmorph, smorph_rulenum, pdes, repsuff, pmorph=['']*10,['']*10,[0]*10,[0]*10,['']*10,['']*10,['']*10
    dspresent=True
    rulenumber, smorph_number, pmorph_number, dub_len, spnt, i,k=0, 0, 0, 0, 0, 0, 0
    go, repcom, rec=0, 0, 0
    suffix, prefix, suffix_index, prefix_index, suffix_rule,prefix_rule, root,\
    tmpgen, isSuffixRoot, suffix_root, root_pos = "","","","","","","","","","",""
    present = "no"

    def __init__(self):

        with open('datasets/stemmer/rootwords',encoding="utf8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]

        for line in lines:
            data={line:line}
            self.ht_root.update(data)

        with open('datasets/stemmer/alt_root.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            roots = line.split(" ")
            data={roots[0]:roots[1]}
            self.alt_root.update(data)
#             data={roots[0]:"null"}
#             self.suffix_exist.update(data)

        with open('datasets/stemmer/suffix.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            suffix = line.split("|")
            data={suffix[0]:suffix[0]}
            self.ht_suffix.update(data)
            if len(suffix)>1:
                data={suffix[0]:suffix[1]}
                self.suffix_ht.update(data)

        with open('datasets/stemmer/suffix_rule.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for i in range(len(lines)):
            nexti=i
            suffix_rules = lines[nexti].split(" ")

            if suffix_rules[0].isdigit():

                data={suffix_rules[0]:suffix_rules[1]}
                self.suffix_type.update(data) #whether the rule is of SFXX or SFX

                data={suffix_rules[0]:suffix_rules[2]}
                self.suf_sub_rule.update(data) #number of sub rule

                data={suffix_rules[0]:suffix_rules[3]}
                self.suffix_morph.update(data) #the morph

                data={suffix_rules[0]:suffix_rules[4]}
                self.suffix_desc.update(data) #the tag of the morph

                data={suffix_rules[0]:suffix_rules[5]}
                self.suffix_ign.update(data) #To ignore in the second parse ('Y'or'N')

                num_sub = int(self.suf_sub_rule.get(suffix_rules[0])) #geting the sub rule
                if (self.suffix_type.get(suffix_rules[0])=="SFX"):
                    for b in range(num_sub):
                        nexti+=1
                        subrule = lines[nexti].split(" ")
                        data={str(suffix_rules[0]) + str(b): subrule[0]}
                        self.suffix_del.update(data)
                        data={str(suffix_rules[0]) + str(b): subrule[1]}
                        self.suffix_ins.update(data)

        with open('datasets/stemmer/prefix.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            prefix = line.split("|")
            data={prefix[0]:prefix[0]}
            self.ht_prefix.update(data)
            if len(prefix)>1:
                data={prefix[0]:prefix[1]}
                self.prefix_tm.update(data)

        with open('datasets/stemmer/prefix_rule.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for i in range(len(lines)):
            nexti=i
            prefix_rules = lines[nexti].split(" ")
            if prefix_rules[0].isdigit():

                data={prefix_rules[0]:prefix_rules[1]}
                self.prefix_type.update(data) #whether the rule is of SFXX or SFX

                data={prefix_rules[0]:prefix_rules[2]}
                self.pre_sub_rule.update(data) #number of sub rule

                data={prefix_rules[0]:prefix_rules[3]}
                self.prefix_morph.update(data) #the morph

                data={prefix_rules[0]:prefix_rules[4]}
                self.prefix_desc.update(data) #the tag of the morph

                num_sub = int(self.suf_sub_rule.get(prefix_rules[0])) #geting the sub rule
                if (self.prefix_type.get(prefix_rules[0])=="PFX"):
                    for b in range(num_sub):
                        nexti+=1
                        subrule = lines[nexti].split(" ")
                        data={str(prefix_rules[0]) + str(b): subrule[0]}
                        self.prefix_del.update(data)
                        data={str(prefix_rules[0]) + str(b): subrule[1]}
                        self.prefix_ins.update(data)

        with open('datasets/stemmer/dub_suffix.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            suffix = line.split(" ")
            data={suffix[0]:suffix[0]}
            self.dub_suffix.update(data)
            data={suffix[0]:suffix[1]}
            self.dub_suffix_morph.update(data)
            data={suffix[0]:suffix[2]}
            self.dub_suffix_desc.update(data)

    def isAltRoot(self,word):
        if word in self.alt_root:
            return True
        else:
            return False

    # get the alternate root
    def getAltRoot(self,word):
        print("\nalternate root found:"+self.alt_root.get(word))

        return self.alt_root.get(word)

    def getSuffixExist(self):
        return self.suffix_exist.get()

    def getSDes(self):
        return self.sdes

    def getSDesat(self,i):
        return self.sdes[i]

    def getPDes(self):
        return self.pdes

    def getSMorph(self):
        return self.smorph

    def getSMorphat(self,i):
        return self.smorph[i]

    def getPMorph(self) :
        return self.pmorph

    def getSMorph_number(self) :
        return self.smorph_number

    def getPMorph_number(self) :
        return self.pmorph_number

    def getRoot(self) :
        return self.root

    def getRuleNumber(self) :
        return self.rulenumber

    def getSuffix_rule(self) :
        return self.suffix_rule

    def isRoot(self,string):
        if string==(self.ht_root.get(string)):
            return True
        return False

    def getRootPos(self) :
        return self.root_pos

    def setRootPos(self,pos):
        self.root_pos = pos

    def setSDes(self,d, i):
        self.sdes[i] = d

    def setSMorph( self,mor, i):
        self.smorph[i] = mor

    def setSuffixRoot(self, m):
        self.isSuffixRoot = m

    def getSuffixRoot(self) :
        return self.isSuffixRoot

    def setSMorph_rulenum(self,i, j):
        self.smorph_rulenum[i] = j

    def getSMorph_rulenum(self,i):
        return self.smorph_rulenum[i]

    def setSubSMorph(self,subnum, i):
        self.subsmorph[i] = subnum

    def getSubSMorph(self,i):
        return self.subsmorph[i]

    def setSecParse( self,i):
        self.parsetwo = i

    def setSMorph_number( self,number):
        self.smorph_number = number

    def setPDes(self, d,  i):
        self.pdes[i] = d

    def setPMorph( self,mor,  i):
        self.pmorph[i] = mor

    def setPMorph_number( self,number):
        self.pmorph_number = number

    def setRoot(self, string):
        self.root = string

    def setRuleNumber( self,i):
        self.rulenumber = i

    def setSuffix_rule(self, suffix_rule):
        self.suffix_rule = suffix_rule

    def generateWord(self,r1, mn):
        print("\ngenerating word")
        q =r1
        t = str(self.smorph_rulenum[mn])
        a = str(self.suffix_del.get(t + str(self.subsmorph[mn])))
        l = len(r1)
        b = int(str(self.suf_sub_rule.get(t)))
        if (self.suffix_type.get(t)==("SFX")):
            for s in range(b):
                if (self.subsmorph[mn] == s) :
                    dot = str(self.suffix_ins.get(t + str(s)))
                    if (dot!=(".")):
                        length = len(dot)
                        q=q.replace(dot,"")
                        q+=a
                        tmpgen = str(q)
                        break
                    else:
                        q+=a
            tmpgen = str(q)
        return tmpgen

    def isASuffix(self,word):
        print("\nVerbs ending with halanta")
        word+="\u094d"
        c = 9998
        i = self.getSMorph_number()
        self.setSMorph_number(i)
        self.setSMorph(str(self.suffix_morph.get(str(c))), i)
        self.setSDes(str(self.suffix_desc.get(str(c))), i)
        self.setRoot(word)

    def isRepeat(self, rn):
        if (str(self.suffix_ign.get(rn))==("Y")):
            return True
        else:
            return False

    def suffixPresent(self,string, o):
        print("\nChecking suffix present or not\n")
        present = "no"
        for rn in range(1,len(string)):
            tmp = string[rn:]
            print ("tmp_suffix:"+tmp)
            if (tmp==(self.ht_suffix.get(tmp))):
                print("\nsuffix found")
                if (self.parsetwo == 1) :
                    if (self.isRepeat(str(self.suffix_ht.get(tmp)))):
                        for j in range(rec):
                            if (self.repsuff[j]==(tmp)) :
                                present = "yes"
                    if (self.present==("no")):
                        self.setRuleNumber(str(int(self.suffix_ht.get(tmp))))
                        return True
                    else :
                        self.setRuleNumber(str(int(self.suffix_ht.get(tmp))))
                        return True
                else:
                    rec = o
                    self.setRuleNumber(str(int(self.suffix_ht.get(tmp))))
                    self.repsuff[rec] = tmp
                    return True
        return False

    def prefixPresent(self,string) :
        print("\nChecking prefix present or not\n")
        for rn in range(len(string)):
            tmp = string[:rn + 1]
            print ("tmp_prefix:"+tmp)
            if (tmp==(self.ht_prefix.get(tmp))) :
                print("\nprefix found")
                self.setRuleNumber(str(int(self.prefix_tm.get(tmp))))
                return True
        return False

    def stripPrefix(self,word):
        print("\nStripping prefix")
        w = word
        b = int(str(self.pre_sub_rule.get(str(self.getRuleNumber()))))
        rulenumber = str(self.getRuleNumber())
        print("rule:"+rulenumber)
        self.setPMorph(str(self.prefix_morph.get(rulenumber)), self.getPMorph_number())
        self.setPDes(str(self.prefix_desc.get(rulenumber)), self.getPMorph_number())
        if (self.prefix_type.get(rulenumber)==("PFX")) :
            for s in range(b):
                print("\nPrefix_del:"+str(self.prefix_del.get(rulenumber + str(s))))
                if (word.startswith(str(self.prefix_del.get(rulenumber + str(s))))):
                    tmp = str(self.prefix_del.get(rulenumber + str(s)))
                    w=w.replace(tmp, "")
                    print("\nfinal: "+w)

                    break
        self.setRoot(str(w))

    def stripSuffix(self,word):
        print("\nStripping suffix")
        w = word
        b = int(str(self.suf_sub_rule.get(str(self.getRuleNumber()))))
        rulenumber = str(self.getRuleNumber())
        self.setSMorph(str(self.suffix_morph.get(rulenumber)), self.getSMorph_number())
        self.setSMorph_rulenum(self.getSMorph_number(), int(rulenumber))
        self.setSDes(str(self.suffix_desc.get(rulenumber)), self.getSMorph_number())
        if (self.suffix_type.get(rulenumber)==("SFX")) :
            print("rule:"+rulenumber)
            for s in range(b):
                lengthw = len(w)
                # print("length:"+str(lengthw))
                print("\nSuffix_del:"+str(self.suffix_del.get(rulenumber + str(s))))
                if (word.endswith(str(self.suffix_del.get(rulenumber + str(s))))):
                    self.setSubSMorph(s, self.getSMorph_number())
                    tmp1 = str(self.suffix_del.get(rulenumber + str(s)))
                    tmp2 = str(self.suffix_ins.get(rulenumber +str(s)))
                    print(tmp1+" "+tmp2)
                    w=w.replace(tmp1, "")
                    if (tmp2!=(".")):
                        w+=tmp2
                        print("not_dot "+tmp2)

                    print("\nfinal: "+w)

                    break;
            self.setRoot(str(w))
        self.setRoot(str(w))
