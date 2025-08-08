class Localidade:

    def __init__(self, json_obj: dict | list):
        self.json_obj: dict | list = json_obj
        self.id: str = self.extrai_id()
        self.nome: str = self.extrai_nome()

    def get_id(self) -> str:
        return self.id

    def get_nome(self) -> str:
        return self.nome

    def extrai_id(self) -> str:
        return self.json_obj["id"]

    def extrai_nome(self) -> str:
        return self.json_obj["nome"]

    def get_json_obj(self) -> dict | list:
        return self.json_obj


class Regiao(Localidade):

    def __init__(self, json_obj):
        super().__init__(json_obj)
        self.sigla: str = self.get_json_obj()["sigla"]

    def get_sigla(self) -> str:
        return self.sigla


class Uf(Localidade):

    def __init__(self, json_obj: dict):
        super().__init__(json_obj)
        self.regiao: Regiao = Regiao(self.json_obj["regiao"])
        self.sigla: str = self.json_obj["sigla"]

    def get_regiao(self) -> Regiao:
        return self.regiao

    def get_sigla(self) -> str:
        return self.sigla


class AglomeracaoUrbana(Localidade):

    def __init__(self, json_obj: dict):
        super().__init__(json_obj)

    def extrai_nome(self) -> str:
        return self.json_obj[0]["nome"]

    def extrai_id(self) -> str:
        return self.json_obj[0]["id"]


class Mesorregiao(Localidade):

    def __init__(self, json_obj: dict):
        super().__init__(json_obj)
        self.uf: Uf = Uf(self.json_obj["UF"])

    def get_uf(self) -> Uf:
        return self.uf


class Microrregiao(Localidade):

    def __init__(self, json_obj: dict):
        super().__init__(json_obj)
        self.mesorregiao: Mesorregiao = Mesorregiao(self.json_obj["mesorregiao"])

    def get_mesorregiao(self) -> Mesorregiao:
        return self.mesorregiao

    def get_uf(self) -> Uf:
        return self.get_mesorregiao().get_uf()


class Municipio(Localidade):

    def __init__(self, json_obj):
        super().__init__(json_obj)
        print(json_obj)
        self.microrregiao: Microrregiao = Microrregiao(
            json_obj=self.json_obj["microrregiao"]
        )

    def get_microrregiao(self) -> Microrregiao:
        return self.microrregiao

    def get_uf(self) -> Uf:
        return self.get_microrregiao().get_uf()


class Distrito(Localidade):

    def __init__(self, json_obj: dict):
        super().__init__(json_obj)
        self.municipio: Municipio = Municipio(self.json_obj[0]["municipio"])

    def get_municipio(self) -> Municipio:
        return self.municipio

    def extrai_nome(self) -> str:
        return self.json_obj[0]["nome"]

    def extrai_id(self) -> str:
        return self.json_obj[0]["id"]

    def get_uf(self) -> Uf:
        return self.get_municipio().get_uf()


def factory(tipo_loc, ibge_data: dict):
    obj = None
    match tipo_loc:
        case "regioes":
            obj = Regiao(json_obj=ibge_data)
        case "aglomeracoes-urbanas":
            obj = AglomeracaoUrbana(json_obj=ibge_data)
        case "distritos":
            obj = Distrito(json_obj=ibge_data)
        case _:
            obj = Localidade(json_obj=ibge_data)

    return obj
