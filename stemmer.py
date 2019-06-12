class Stemmer:
    suf_sub_rule,suffix_del,suffix_exist, suffix_look_posi, suffix_look_char, suffix_desc, \
    suffix_ins ,suffix_ins_posi, suffix_morph, suffix_type, suffix_ign, dub_suffix ,dub_suffix_morph,\
    dub_suffix_desc, pre_sub_rule, prefix_del, prefix_desc, prefix_ins, prefix_morph, prefix_type,\
    ht_root, ht_root_pos, suffix_ht, alt_root, ht_suffix, prefix_tm, ht_prefix=dict(),dict(),dict(),\
    dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),\
    dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict(),dict()

    def __init__(self):
        with open('datasets/stemmer/rootwords',encoding="utf8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]

        for line in lines:
            data={line:line}
            ht_root.update(data)

        with open('datasets/stemmer/alt_root.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            roots = line.split(" ")
            data={roots[0]:roots[1]}
            alt_root.update(data)
            data={roots[0]:"null"}
            suffix_exist.update(data)

        with open('datasets/stemmer/suffix.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            suffix = line.split("|")
            data={suffix[0]:suffix[0]}
            ht_suffix.update(data)
            if len(suffix)>1:
                data={suffix[0]:suffix[1]}
                suffix_ht.update(data)

        with open('datasets/stemmer/suffix_rule.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for i in range(len(lines)):
            nexti=i
            suffix_rules = lines[nexti].split(" ")

            if suffix_rules[0].isdigit():

                data={suffix_rules[0]:suffix_rules[1]}
                suffix_type.update(data) #whether the rule is of SFXX or SFX

                data={suffix_rules[0]:suffix_rules[2]}
                suf_sub_rule.update(data) #number of sub rule

                data={suffix_rules[0]:suffix_rules[3]}
                suffix_morph.update(data) #the morph

                data={suffix_rules[0]:suffix_rules[4]}
                suffix_desc.update(data) #the tag of the morph

                data={suffix_rules[0]:suffix_rules[5]}
                suffix_ign.update(data) #To ignore in the second parse ('Y'or'N')

                num_sub = int(suf_sub_rule.get(suffix_rules[0])) #geting the sub rule
                if (suffix_type.get(suffix_rules[0])=="SFX"):
                    for b in range(num_sub):
                        nexti+=1
                        subrule = lines[nexti].split(" ")
                        data={str(suffix_rules[0]) + str(b): subrule[0]}
                        suffix_del.update(data)
                        data={str(suffix_rules[0]) + str(b): subrule[1]}
                        suffix_ins.update(data)

        with open('datasets/stemmer/prefix.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            prefix = line.split("|")
            data={prefix[0]:prefix[0]}
            ht_prefix.update(data)
            if len(prefix)>1:
                data={prefix[0]:prefix[1]}
                prefix_tm.update(data)

        with open('datasets/stemmer/prefix_rule.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for i in range(len(lines)):
            nexti=i
            prefix_rules = lines[nexti].split(" ")

            if prefix_rules[0].isdigit():

                data={prefix_rules[0]:prefix_rules[1]}
                prefix_type.update(data) #whether the rule is of SFXX or SFX

                data={prefix_rules[0]:prefix_rules[2]}
                pre_sub_rule.update(data) #number of sub rule

                data={prefix_rules[0]:prefix_rules[3]}
                prefix_morph.update(data) #the morph

                data={prefix_rules[0]:prefix_rules[4]}
                prefix_desc.update(data) #the tag of the morph

                num_sub = int(suf_sub_rule.get(prefix_rules[0])) #geting the sub rule
                if (prefix_type.get(prefix_rules[0])=="PFX"):
                    for b in range(num_sub):
                        nexti+=1
                        subrule = lines[nexti].split(" ")
                        data={str(prefix_rules[0]) + str(b): subrule[0]}
                        prefix_del.update(data)
                        data={str(prefix_rules[0]) + str(b): subrule[1]}
                        prefix_ins.update(data)


        with open('datasets/stemmer/dub_suffix.txt',encoding="UTF8") as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            suffix = line.split(" ")
            data={suffix[0]:suffix[0]}
            dub_suffix.update(data)
            data={suffix[0]:suffix[1]}
            dub_suffix_morph.update(data)
            data={suffix[0]:suffix[2]}
            dub_suffix_desc.update(data)
