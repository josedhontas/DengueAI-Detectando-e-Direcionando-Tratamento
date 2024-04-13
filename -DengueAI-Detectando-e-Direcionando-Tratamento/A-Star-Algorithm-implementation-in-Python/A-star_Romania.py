preciso de uma ideia de como fazer para usar o A* em um problema onde eu tenho uma base de dados sobre pessoas com dengue e uma outra base de hospitais, preciso entender com eu aplicaria o A* preciso de ideias de implementação

def printoutput(start, end, path, distance, expandedlist):
    finalpath = []
    i = end
    while (path.get(i) != None):
        finalpath.append(i)
        i = path[i]
    finalpath.append(start)
    finalpath.reverse()
    print("Agoritmo A-star")
    print("\de quem  => para quem")
    print("=============================================== ========")
    print("Lista de cidades que estão expandidas: "  + str(expandedlist))
    print("Número total de cidades expandidas: " + str(len(expandedlist)))
    print("=============================================== ========")
    print("Cidades no caminho final: "+ str(finalpath))
    print("O número total de cidades no caminho final é: " + str(len(finalpath)))
    print("Custo total: " + str(distance[end]))

def main():
    src = "Arad"
    dst = "Bucharest"
    makedict()
    astar(src, dst)

if __name__ == "__main__" :
    main()
