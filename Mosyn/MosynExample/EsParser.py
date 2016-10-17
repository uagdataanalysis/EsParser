# -*- coding: iso-8859-15 -*-
from copy import deepcopy

import mosyn
from Model.DescripcionPalabra import DescripcionPalabra
from Model.Oracion import Oracion


def main():
    dictionary = mosyn.MorphologicalDictionary("/home/christian/Documentos/mosynapi-master/mosyn/dict/spanish_dict.csv")
    dictionary.load()
    manager = mosyn.AnalysisManager(dictionary)

    processed_data = manager.parse_string_to_eagles(u"el ni�o que me salud� de all�")

    oracion = []
    aux = []
    palabras = []
    for labels in processed_data:
        for label in labels:
            palabras.append(DescripcionPalabra(labels[0].get_lema(), label.get_category(), label.get_number(),
                                               label.get_type(), label.get_gender()))

    l = 0

    while l < len(palabras):
        palabras1 = []
        if l != (len(palabras) - 1) and palabras[l].lema == palabras[l + 1].lema:
            palabras1.append(palabras[l + 1])
            l += 1
        palabras1.append(palabras[l])
        oracion.append(deepcopy(palabras1))
        l += 1
    i = 0
    aux1 = ''
    while i <= len(oracion) - 1:
        for j in xrange(0, len(oracion[i])):
            aux1 = ''
            if oracion[i][j].getCategoria() == 'nombre' \
                    or oracion[i][j].getCategoria() == 'pronombre':
                for k in xrange(0, len(oracion[i + 1])):
                    if oracion[i + 1][k].getCategoria() == 'nombre':
                        i += 1
                        break
                aux1 = 'SN'
            elif oracion[i][j].getCategoria() == 'determinante' \
                    or oracion[i][j].getCategoria() == 'conjuncion':
                for k in xrange(0, len(oracion[i + 1])):
                    if oracion[i + 1][k].getCategoria() == 'nombre' \
                            or oracion[i + 1][k].getCategoria() == 'pronombre' \
                            or oracion[i + 1][k].getCategoria() == 'adjetivo':
                        aux1 = 'SD'
                        i += 1
                        break
            elif oracion[i][j].getCategoria() == 'verbo':
                aux1 = 'V'
            elif oracion[i][j].getCategoria() == 'adjetivo':
                aux1 = 'SD'
            elif oracion[i][j].getCategoria() == 'adverbio':
                for k in xrange(0, len(oracion[i + 1])):
                    if oracion[i + 1][k].getCategoria() == 'adjetivo':
                        aux1 = 'SD'
                        i += 1
            elif oracion[i][j].getCategoria() == 'preposicion':
                for k in xrange(0, len(oracion[i + 1])):
                    if oracion[i + 1][k].getCategoria() == 'nombre' \
                            or oracion[i + 1][k].getCategoria() == 'pronombre' \
                            or oracion[i + 1][k].getCategoria() == 'adjetivo' \
                            or oracion[i + 1][k].getCategoria() == 'adverbio':
                        aux1 = 'P'
                        i += 1
                        break
            else:
                aux1 = ''
            i += 1
            if aux1 != '':
                break
        if aux1 != '':
            aux.append(aux1)
        else:
            return False

    return VerificarOracion(aux)


def VerificarOracion(oracion):
    while len(oracion) != 1:
        i = 0
        aux1 = []
        if len(oracion) % 2 != 0:
            oracion.append("")
        while i < len(oracion) - 1:
            aux = ""
            if (oracion[i] == "SN" and oracion[i + 1] == "SD") \
                    or (oracion[i] == "SD" and oracion[i + 1] == "SN"):
                aux = "SD"
                i += 1
            elif (oracion[i] == "SN" and oracion[i + 1] == "SN") \
                    or oracion[i] == "SN":
                aux = "SN"
            elif (oracion[i] == "SD" and oracion[i + 1] == "V") \
                    or (oracion[i] == "V") \
                    or (oracion[i] == "ST"):
                aux = "ST"
                i += 1
            elif oracion[i] == 'C' and oracion[i + 1] == 'ST':
                aux = "SC"
            elif oracion[i] == "SD" and oracion[i + 1] == "SC":
                aux = "SD"
            elif oracion[i] == "SD" and oracion[i + 1] == "ST":
                aux = "O"
            if aux != "":
                aux1.append(aux)
            i += 1
        oracion = deepcopy(aux1)
    return oracion


def VerificaTiempo(oracion):
    return False


if __name__ == '__main__':
    x = main()
    print x