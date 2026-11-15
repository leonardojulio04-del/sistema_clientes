
from sqlalchemy import create_engine, String, Integer, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship, sessionmaker


# 1. Configuração do banco de dados
engine = create_engine("sqlite:///clientes.db", echo=False)

Session = sessionmaker(bind=engine)


# 2. Criação da classe base
class Base(DeclarativeBase):
    pass


# 3. Tabela de clientes
class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    telefone: Mapped[str] = mapped_column(String(20))

    # Relacionamento com endereços
    enderecos: Mapped[list["Endereco"]] = relationship(
        back_populates="cliente",
        cascade="all, delete-orphan"
    )


# 4. Tabela de endereços
class Endereco(Base):
    __tablename__ = "enderecos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rua: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    cep: Mapped[str] = mapped_column(String(10))

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"), nullable=False
    )

    # Relacionamento com cliente
    cliente: Mapped["Cliente"] = relationship(
        back_populates="enderecos"
    )


# 5. Criação das tabelas no banco
Base.metadata.create_all(engine)


# 6. CREATE - Cadastrar cliente e endereço
def criar_cliente():
    with Session() as session:
        nome = input("Nome do cliente: ")
        email = input("E-mail: ")
        telefone = input("Telefone: ")

        cliente = Cliente(
            nome=nome,
            email=email,
            telefone=telefone
        )

        rua = input("Rua: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")

        endereco = Endereco(
            rua=rua,
            cidade=cidade,
            estado=estado,
            cep=cep
        )

        cliente.enderecos.append(endereco)

        session.add(cliente)
        session.commit()

        print("\nCliente cadastrado com sucesso!")


# 7. READ - Listar clientes
def listar_clientes():
    with Session() as session:
        clientes = session.scalars(
            select(Cliente).order_by(Cliente.id)
        ).all()

        print("\n--- LISTA DE CLIENTES ---")

        for cliente in clientes:
            print(
                f"ID: {cliente.id} | "
                f"Nome: {cliente.nome} | "
                f"E-mail: {cliente.email} | "
                f"Telefone: {cliente.telefone}"
            )


# 8. UPDATE - Atualizar cliente
def atualizar_cliente():
    with Session() as session:
        id_cliente = int(input("Digite o ID do cliente: "))

        cliente = session.get(Cliente, id_cliente)

        if cliente:
            print("Deixe vazio o campo que não deseja alterar.")

            nome = input(f"Novo nome ({cliente.nome}): ")
            email = input(f"Novo e-mail ({cliente.email}): ")
            telefone = input(
                f"Novo telefone ({cliente.telefone}): "
            )

            if nome:
                cliente.nome = nome

            if email:
                cliente.email = email

            if telefone:
                cliente.telefone = telefone

            session.commit()
            print("\nCliente atualizado com sucesso!")
        else:
            print("\nCliente não encontrado!")


# 9. DELETE - Excluir cliente
def excluir_cliente():
    with Session() as session:
        id_cliente = int(input("Digite o ID do cliente: "))

        cliente = session.get(Cliente, id_cliente)

        if cliente:
            session.delete(cliente)
            session.commit()

            print("\nCliente excluído com sucesso!")
            print("Seus endereços também foram excluídos.")
        else:
            print("\nCliente não encontrado!")


# 10. JOIN - Consultar clientes e seus endereços
def consultar_clientes_enderecos():
    with Session() as session:

        consulta = (
            select(Cliente, Endereco)
            .join(
                Endereco,
                Cliente.id == Endereco.cliente_id
            )
            .order_by(Cliente.id)
        )

        resultados = session.execute(consulta).all()

        print("\n--- CLIENTES E SEUS ENDEREÇOS ---")

        for cliente, endereco in resultados:
            print(f"\nID: {cliente.id}")
            print(f"Nome: {cliente.nome}")
            print(f"E-mail: {cliente.email}")
            print(f"Telefone: {cliente.telefone}")
            print(f"Rua: {endereco.rua}")
            print(f"Cidade: {endereco.cidade}")
            print(f"Estado: {endereco.estado}")
            print(f"CEP: {endereco.cep}")


# 11. Menu principal
def menu():
    while True:
        print("\n====== SISTEMA DE CLIENTES ======")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Excluir cliente")
        print("5 - Consultar clientes e endereços")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        try:
            if opcao == "1":
                criar_cliente()

            elif opcao == "2":
                listar_clientes()

            elif opcao == "3":
                atualizar_cliente()

            elif opcao == "4":
                excluir_cliente()

            elif opcao == "5":
                consultar_clientes_enderecos()

            elif opcao == "0":
                print("Encerrando o sistema...")
                break

            else:
                print("Opção inválida!")

        except ValueError:
            print("Erro: informe um valor válido.")

        except Exception as erro:
            print(f"Erro ao executar operação: {erro}")


# 12. Executar o sistema
if __name__ == "__main__":
    menu()
