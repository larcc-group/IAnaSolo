//Auditor
const csv = require("csvtojson");
const fs = require('fs');


const csvFilePath = './Dados/AnalisesDeSoloLaboratorio.csv';
const jsonFilePath = './Dados/resultados.json';

let json = fs.readFileSync(jsonFilePath);

const jsonResultImages = JSON.parse(json)
let totalReconhecidas = 0;
let totalMinimoReconhecidas = 0;
let totalFalhas = 0;
let totalElementos = 0;

csv()
    .fromFile(csvFilePath)
    .then((jsonObj) => {
        // console.log(jsonObj);


        jsonResultImages.forEach(element => {

            // console.log(element.dadosExtraidos);
            totalElementos += 1;
           let encontrou = false;
           jsonObj.forEach((item) => {

                if (item.AMO_CODIGO == element.dadosExtraidos.amostra) {
                    // console.log(item);
                        encontrou = true;

                        if (item) {
                            // console.log(element, item)
                            validacao(element, item).then(totalElements => {
            
                                //Na tabela são 26, porém a o numero da amostra se repete.
                                if (totalElements == 25) {
                                    totalReconhecidas += 1;
                                } else if (totalElements >= 20) {
                                    totalMinimoReconhecidas += 1;

                                    if(totalElements == 24){

                                    console.log(element, item)

                                    }

                                } else {
                                    totalFalhas += 1;
                                }
            
                                console.log("TotalElements: ", totalElements);
            
            
                                console.log("Reconhecidas: ", totalReconhecidas, " MinimoReconhecidas: ", totalMinimoReconhecidas, " Falhas: ", totalFalhas, " Total: ", totalElementos);
            
            
                            }).catch(error => {
                                console.log(error);
                                totalFalhas += 1;
                            });
                        }else{
                            totalFalhas += 1
                        }

                    
                    return;

                }
                

            });

            if (!encontrou){
                totalFalhas += 1;
            }

        
        });

    })

function validacao(json, jsonAnalise) {

    return new Promise((resolve, reject) => {
        console.log("Amostra", jsonAnalise.AMO_CODIGO)
        try {

            let count = 1; //Inicia em 1 pq se chegou aqui o numero da amostra já identificou
        
            if (json.dadosExtraidos.area_ha) {

                console.log(json.dadosExtraidos.area_ha)
                count += 1
            
            }else{
                console.log("erro", json.dadosExtraidos.area_ha)
            }

            if (jsonAnalise.Argila == "0" || jsonAnalise.Argila.indexOf(json.dadosExtraidos.argila.replace(",","."),0) != -1) {

                console.log("Achou", json.dadosExtraidos.argila, jsonAnalise.Argila)
                count += 1
            
            }else{
                console.log("Errou", json.dadosExtraidos.argila, jsonAnalise.Argila)
            }

            if (jsonAnalise.ClasseTextural == "0" || jsonAnalise.ClasseTextural.indexOf(json.dadosExtraidos.classe_textural.replace(",","."),0) != -1) {

                console.log(json.dadosExtraidos.classe_textural, jsonAnalise.ClasseTextural)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.classe_textural, jsonAnalise.ClasseTextural)
            }

            if ((jsonAnalise.pH_H2O == "0" || jsonAnalise.pH_H2O == undefined) || jsonAnalise.pH_H2O.indexOf(json.dadosExtraidos.ph_H20.replace(",","."),0) != -1) {

                console.log(json.dadosExtraidos.pH_H2O, jsonAnalise.ph_H20)
                count += 1
            }else{
                console.log("Error",json.dadosExtraidos.H2O, jsonAnalise.H2O)
            }


            if (jsonAnalise.Indice_SMP == "0" || jsonAnalise.Indice_SMP.indexOf(json.dadosExtraidos.indice_SMP.replace(",","."), 0) != -1) {

                console.log(json.dadosExtraidos.indice_SMP, jsonAnalise.Indice_SMP)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.indice_SMP, jsonAnalise.Indice_SMP)
            }

            if (jsonAnalise.M_O == "0" || jsonAnalise.M_O.indexOf(json.dadosExtraidos.m_o.replace(",","."), 0) != -1) {

                console.log(json.dadosExtraidos.m_o , jsonAnalise.M_O)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.m_o , jsonAnalise.M_O)
            }

            if (jsonAnalise.P == "0" || jsonAnalise.P.indexOf(json.dadosExtraidos.p.replace(",","."), 0) != -1) {

                console.log(json.dadosExtraidos.p , jsonAnalise.P)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.p , jsonAnalise.P, jsonAnalise.P.indexOf(json.dadosExtraidos.p.replace(",","."), 0))
            }

            if (jsonAnalise.K == "0" || jsonAnalise.K.indexOf(json.dadosExtraidos.k.replace(",","."),0) != -1) {

                console.log(json.dadosExtraidos.k , jsonAnalise.K)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.k , jsonAnalise.K)
            }


            if (jsonAnalise.Ca == "0" || jsonAnalise.Ca.indexOf(json.dadosExtraidos.ca.replace(",","."), 0) != -1) {

                console.log(json.dadosExtraidos.ca , jsonAnalise.Ca)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.ca , jsonAnalise.Ca)
            }

            if (jsonAnalise.Mg == "0" || jsonAnalise.Mg.indexOf(json.dadosExtraidos.mg.replace(",","."), 0) != -1) {

                console.log(json.dadosExtraidos.mg , jsonAnalise.Mg)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.mg , jsonAnalise.Mg)
            }

            if (jsonAnalise.Al == "0"|| jsonAnalise.Al.indexOf(json.dadosExtraidos.al.replace(",","."),0) != -1) {

                console.log(json.dadosExtraidos.al , jsonAnalise.Al)
                count += 1
            }else{
                console.log("Error" ,json.dadosExtraidos.al , jsonAnalise.Al)

            }

            if (jsonAnalise.H_AL == "0" || jsonAnalise.H_AL.indexOf(json.dadosExtraidos.h_al.replace(",","."),0) != -1) {

                console.log(json.dadosExtraidos.h_al ,jsonAnalise.H_AL)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.h_al ,jsonAnalise.H_AL)
            }

            if (jsonAnalise.CTCEfetiva == "0" || jsonAnalise.CTCEfetiva.indexOf(json.dadosExtraidos.ctc_efetiva.replace(",","."),0) != -1) {

                console.log(json.dadosExtraidos.ctc_efetiva , jsonAnalise.CTCEfetiva)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.ctc_efetiva , jsonAnalise.CTCEfetiva)
            }

            if (jsonAnalise.CTCPH == "0" || jsonAnalise.CTCPH.indexOf(json.dadosExtraidos.ctc_ph.replace(",","."),0) != -1) {

                console.log(json.dadosExtraidos.ctc_ph,jsonAnalise.CTCPH)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.ctc_ph,jsonAnalise.CTCPH)
            }

            if ((jsonAnalise.SaturacaoBases == "0" ) || jsonAnalise.SaturacaoBases.indexOf(json.dadosExtraidos.saturacao_bases.replace(",","."),0) != -1) {

                console.log(json.dadosExtraidos.saturacao_bases ,jsonAnalise.SaturacaoBases)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.saturacao_bases ,jsonAnalise.SaturacaoBases)
            }

            if (jsonAnalise.SaturacaoAl == "0" || jsonAnalise.SaturacaoAl.indexOf(json.dadosExtraidos.saturacao_al.replace(",","."), 0) != -1) {

                console.log(json.dadosExtraidos.saturacao_al ,jsonAnalise.SaturacaoAl)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.saturacao_al ,jsonAnalise.SaturacaoAl)
            }

            if (jsonAnalise.S == "0" || jsonAnalise.S.indexOf(json.dadosExtraidos.s.replace(",","."), 0) != -1) {

                console.log(json.dadosExtraidos.s ,jsonAnalise.S)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.s ,jsonAnalise.S)
            }


            if (jsonAnalise.B == "0" || jsonAnalise.B.indexOf(json.dadosExtraidos.b.replace(",","."),0) != -1) {

                console.log(json.dadosExtraidos.b,jsonAnalise.B)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.b,jsonAnalise.B)
            }

            if (jsonAnalise.Cu == "0" || jsonAnalise.Cu.indexOf(json.dadosExtraidos.cu.replace(",","."),0) != -1) {

                console.log(json.dadosExtraidos.cu ,jsonAnalise.Cu)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.cu ,jsonAnalise.Cu)
            }

            if (jsonAnalise.Zn == "0" || jsonAnalise.Zn.indexOf(json.dadosExtraidos.zn.replace(",","."), 0) != -1) {

                console.log(json.dadosExtraidos.zn ,jsonAnalise.Zn)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.zn ,jsonAnalise.Zn)
            }

            if (jsonAnalise.Mn == "0" || jsonAnalise.Mn.indexOf(json.dadosExtraidos.mn.replace(",","."), 0) != -1) {

                console.log(json.dadosExtraidos.mn, jsonAnalise.Mn)
                count += 1
            }else{
                console.log("Error", json.dadosExtraidos.mn, jsonAnalise.Mn)
            }

            if (json.dadosExtraidos.mo) {

                console.log(json.dadosExtraidos.mo)
                count += 1
            }

            if (json.dadosExtraidos.fe) {

                console.log(json.dadosExtraidos.fe)
                count += 1
            }

            if (json.dadosExtraidos.na) {

                console.log(json.dadosExtraidos.na)
                count += 1
            }

            //retorno a quantidade de elementos válidados com sucesso.
            resolve(count)


        } catch (error) {
            reject(error)
        }

    })

}
