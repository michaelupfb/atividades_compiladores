// GRUPO:
// - ARTHUR MIRANDA TAVARES
// - LUCAS FARIAS DE MEDEIROS
// - MIHCAEL DA CUNHA PINHO
// - RENAN GONDIM DIAS DE ALBUQUERQUE

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

int main() {

    ifstream arquivo_modelo_assembly("modelo.s"); // Abre o arquivo

    if (!arquivo_modelo_assembly) { // Verifica se o arquivo foi aberto com sucesso
        std::cerr << "Erro ao abrir o arquivo!" << std::endl;
        return 1;
    }

    vector<std::string> linhas_assembly; // Vetor para armazenar as linhas
    string linha;

    while (getline(arquivo_modelo_assembly, linha)) { // Lê linha por linha
        linhas_assembly.push_back(linha); // Adiciona a linha ao vetor
    }

    arquivo_modelo_assembly.close();

    ifstream codigo("p1.ci");

    string numero;

    getline(codigo, numero);

    bool somenteNumeros = all_of(numero.begin(), numero.end(), ::isdigit);

    if (!somenteNumeros) {
        cout << "Insira um valor inteiro não negativo!";
    }

    vector<std::string> instrucao_assembly = {"mov $" + numero + ", %rax"};

    for (int i = 0; i < instrucao_assembly.size(); i++) {
        linhas_assembly.insert(linhas_assembly.begin() + 9 + i, instrucao_assembly[i]);
    }

    std::ofstream arquivo_assembly("p1.s");

    for (int i = 0; i < linhas_assembly.size(); i++) {
        arquivo_assembly << linhas_assembly[i];
        arquivo_assembly << "\n";
    }
    
    return 0;
}
