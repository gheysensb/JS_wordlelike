        function entree(mot,dico,nombrelettre){
            if (mot.length==nombrelettre & dico.includes(mot)){
                $(".error").html("");
                return true;
            }
            else{
                $(".error").html("<h1>Le mot n'est pas dans le dictionnaire !</h1>");
                return false;
            }
        }
        function validation(i,testmot,motatrouve,latentative){
            if(testmot[i]==motatrouve[i]){
                latentative.push([testmot[i],"2"]);
            }
            else if (motatrouve.includes(testmot[i])){
                latentative.push([testmot[i],"1"]);
            }
            else{
                latentative.push([testmot[i],"0"]);
            }
        }

        function motvalid(testmot,motatrouve,nbtentative,nbessai){
            if (testmot == motatrouve){
                return "win";

            }



            else if(testmot != motatrouve & nbtentative == nbessai){
                return "loose";
            }
            else{
                return "nextstep";
            }
        }



        function validationfinale(testmot,motatrouve,latentative){
            let OCURENCE = [];
            let Lettres = [];
            for(i=0;i<motatrouve.length;i++){
                if((Lettres.includes(motatrouve[i]))==false){
                    Lettres.push(motatrouve[i]);
                    let compteur = 1 ;
                    for (j=i+1;j<motatrouve.length;j++){
                        if(motatrouve[j]==motatrouve[i]){
                            compteur++;
                        }
                    }
                    OCURENCE.push(compteur);
                }
            }
            for(k=0;k<latentative.length;k++){
                if(latentative[k][1]=='2'){
                    let indicelettre = Lettres.indexOf(latentative[k][0]);
                    OCURENCE[indicelettre]=OCURENCE[indicelettre]-1;
                }
            }
            for(m=0;m<latentative.length;m++){
                if(latentative[m][1]=='1'){
                    let indicelettre2 = Lettres.indexOf((latentative[m][0]));
                    if(OCURENCE[indicelettre2]<1){
                        latentative[m][1]='0';
                    }
                    else{
                        OCURENCE[indicelettre2] = OCURENCE[indicelettre2]-1 ;
                    }
                }
            }
        }


