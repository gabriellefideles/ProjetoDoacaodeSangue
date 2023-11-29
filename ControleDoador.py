
mport cx_Oracle

class Doador:
    def _init_(self, doador_id, nome, idade, tipo_sanguineo, data_ultima_doacao):
        self.doador_id = doador_id
        self.nome = nome
        self.idade = idade
        self.tipo_sanguineo = tipo_sanguineo
        self.data_ultima_doacao = data_ultima_doacao

    def to_string(self):
        return f"Doador ID: {self.doador_id}, Nome: {self.nome}, Idade: {self.idade}, Tipo Sanguíneo: {self.tipo_sanguineo}, Última Doação: {self.data_ultima_doacao}"

class Doacao:
    def _init_(self, doacao_id, doador_id, data_doacao, quantidade_ml):
        self.doacao_id = doacao_id
        self.doador_id = doador_id
        self.data_doacao = data_doacao
        self.quantidade_ml = quantidade_ml

    def to_string(self):
        return f"Doação ID: {self.doacao_id}, Doador ID: {self.doador_id}, Data: {self.data_doacao}, Quantidade (ml): {self.quantidade_ml}"

class ControladorBancoDeDados:
    def _init_(self, conexao):
        self.conexao = conexao

    def inserir_doador(self, doador):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("INSERT INTO Doadores VALUES (:1, :2, :3, :4, :5)",
                           (doador.doador_id, doador.nome, doador.idade, doador.tipo_sanguineo, doador.data_ultima_doacao))
            self.conexao.commit()
        except cx_Oracle.Error as erro:
            print(f"Erro ao inserir doador: {erro}")
            self.conexao.rollback()
        finally:
            cursor.close()

    def inserir_doacao(self, doacao):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("INSERT INTO Doacoes VALUES (:1, :2, :3, :4)",
                           (doacao.doacao_id, doacao.doador_id, doacao.data_doacao, doacao.quantidade_ml))
            self.conexao.commit()
        except cx_Oracle.Error as erro:
            print(f"Erro ao inserir doação: {erro}")
            self.conexao.rollback()
        finally:
            cursor.close()

class Relatorios:
    @staticmethod
    def relatorio_total_doacoes_por_tipo_sanguineo(conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT tipo_sanguineo, COUNT(*) as total_doacoes FROM Doadores GROUP BY tipo_sanguineo")
            resultado = cursor.fetchall()
            return resultado
        except cx_Oracle.Error as erro:
            print(f"Erro ao gerar relatório_total_doacoes_por_tipo_sanguineo: {erro}")
        finally:
            cursor.close()

    @staticmethod
    def relatorio_detalhes_doacao_com_doador(conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT d.nome AS nome_doador, do.data_doacao, do.quantidade_ml FROM Doacoes do JOIN Doadores d ON do.doador_id = d.doador_id")
            resultado = cursor.fetchall()
            return resultado
        except cx_Oracle.Error as erro:
            print(f"Erro ao gerar relatório_detalhes_doacao_com_doador: {erro}")
        finally:
            cursor.close()

class Config:
    MENU_ENTIDADES = {
        1: 'Doador',
        2: 'Doação'
    }

    MENU_RELATORIOS = {
        1: 'Total de Doações por Tipo Sanguíneo',
        2: 'Detalhes da Doação com Doador'
    }

class SplashScreen:
    def show(self):
        print("*************")
        print("* Sistema de Gestão de Doação de Sangue *")
        print("* Grupo: [Nomes dos componentes do grupo] *")
        print("* Professor: [Nome do professor] *")
        print("* Disciplina: [Nome da disciplina] *")
        print("* Semestre: [Número do semestre] *")
        print("*************")

def menu_relatorios(conexao):
    while True:
        print("Menu Relatórios:")
        print("1. Total de Doações por Tipo Sanguíneo")
        print("2. Detalhes da Doação com Doador")
        print("3. Voltar")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            relatorio_total_doacoes_por_tipo_sanguineo(conexao)
        elif opcao == 2:
            relatorio_detalhes_doacao_com_doador(conexao)
        elif opcao == 3:
            break
        else:
            print("Opção inválida. Tente novamente.")

def relatorio_total_doacoes_por_tipo_sanguineo(conexao):
    relatorio = Relatorios.relatorio_total_doacoes_por_tipo_sanguineo(conexao)
    print("Relatório: Total de Doações por Tipo Sanguíneo")
    for tipo_sanguineo, total_doacoes in relatorio:
        print(f"Tipo Sanguíneo: {tipo_sanguineo}, Total de Doações: {total_doacoes}")

def relatorio_detalhes_doacao_com_doador(conexao):
    relatorio = Relatorios.relatorio_detalhes_doacao_com_doador(conexao)
    print("Relatório: Detalhes da Doação com Doador")
    for nome_doador, data_doacao, quantidade_ml in relatorio:
        print(f"Nome do Doador: {nome_doador}, Data da Doação: {data_doacao}, Quantidade (ml): {quantidade_ml}")

def main():
    conexao = cx_Oracle.connect('seu_usuario/sua_senha@localhost:1521/seu_banco')

    splash = SplashScreen()
    splash.show()

    while True:
        print("Menu Principal:")
        print("1. Menu Doador")
        print("2. Menu Doação")
        print("3. Menu Relatórios")
        print("4. Sair")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            menu_doador(conexao)
        elif opcao == 2:
            menu_doacao(conexao)
        elif opcao == 3:
            menu_relatorios(conexao)
        elif opcao == 4:
            conexao.close()
            break
        else:
            print("Opção inválida. Tente novamente.")

if _name_ == "_main_":
    main()

def menu_doador(conexao):
    controlador_banco_dados = ControladorBancoDeDados(conexao)

    while True:
        print("Menu Doador:")
        print("1. Cadastrar Doador")
        print("2. Voltar")