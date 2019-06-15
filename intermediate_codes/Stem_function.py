from stemmer import Stemmer
st=Stemmer()
def stem(tokens):
    rep,i,k,repc=0,0,0,0
    new=[]
    unrecog=[]
    count=1
    for token in tokens:
        p="yes"
        i,k = 0,0 #no. of suffix and prefix found
        print("\nUnstemmed input token"+str(count)+":"+token)
        orig_token=token
        end=False
        while (not end):
            print("Checking root word or not")
            if (st.isRoot(token) or( st.isAltRoot(token) and i>0)):
                print("comdition1")
                if( st.isAltRoot(token) and i>0):
                    st.setRoot(st.getAltRoot(token))

                else:
                    st.setRoot(token)
                    print("\nRoot word found:"+token)
                end=True

            elif (st.isRoot(token + "\u094d")) :
                print("comdition2")

                i+=1
                st.setSMorph_number(i)
                st.isASuffix(token)
                token = st.getRoot()


            elif (token.endswith("\u094d") and st.isRoot(token[:len(token)-1])):
                print("comdition3")
                token=token[:len(token)-1]
                st.setRoot(token)

            elif (st.suffixPresent(token,i)) :
                print("comdition4")
                i+=1
                st.setSMorph_number(i)
                st.stripSuffix(token)
                token = st.getRoot()

            elif (st.prefixPresent(token)) :
                print("comdition5")
                k+=1
                st.setPMorph_number(k)
                st.stripPrefix(token)
                token = st.getRoot()

            else:
                print("\nRecombining suffix")

    #           if prefix and suffix present
                if (k > 0 and i > 0) :
                    print("comdition6:bot suffix and prefix found previously")

                    a = st.getPMorph()
                    print("PMorph:"+str(a))
                    for k1 in range(k,0,-1):
                        tmp = token
                        for l in range(i,0,-1):
                            tm = st.generateWord(tmp, l)
                            print("generated word: "+tm)

                            if (st.isRoot(tm) or ( st.isAltRoot(tm) and i>0)):
                                bk = 1
                                st.setSMorph_number(l - 1)
                                st.setPMorph_number(k)
                                if(( st.isAltRoot(tm) and i>0)):
                                    st.setRoot(st.getAltRoot(tm))
                                else:
                                    st.setRoot(tm)
                                token = st.getRoot()
                                break
                            else:
                                bk = 0
                                tmp = tm

                        if (bk == 1) :
                            break


                        if (k1 > 1):
                            token = a[k1] + token


                    if (bk != 1) :
                        st.setRoot("unrecognized")

                        k = 0


                else:
                    print("comdition7:unrecognized")

                    st.setRoot("unrecognized")


                if (st.getRoot()==("unrecognized")):
                    rep+=1

                    repeat = 0
    #               for the second parse
                    if (rep == 1) :
    #                   check for if the any rulenumber of the suffix contains repeat sign "Y"
                        for l in range(i,0,-1):
                            if (st.isRepeat(str(st.getSMorph_rulenum(l)))):
                                repeat = 1
                                break #//for any suffix that has a repeat sign.
                            else:
                                repeat = 0


    #               if any rulenumber has the suffix content as repeat sign"Y"
                    if (repeat == 1) :
                        token = origtoken
                        st.setPMorph_number(0)
                        st.setSMorph_number(0)
                        i = 0
                        k = 0
                        st.setSecParse(rep)
                    else:
                        break
        if(st.getRoot()==("unrecognized")):
            unrecog.append(orig_token)
            new.append(orig_token)
            print("\nfinal token (couldnt stem):"+orig_token)

        else:
            new.append(st.getRoot())
            print("\nfinal stemmed token:"+st.getRoot())
        count+=1
    return new
