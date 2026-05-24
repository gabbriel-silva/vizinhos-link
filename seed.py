"""
seed.py — Popula o banco de dados com usuários e posts de exemplo.
Execute UMA VEZ com: python seed.py
"""

from app import app, db
from app import User, Post, Comment
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed():
    with app.app_context():
        db.create_all()

        Comment.query.delete()
        Post.query.delete()
        User.query.delete()
        db.session.commit()
        print("Banco limpo.")

        # --- USUÁRIOS ---
        usuarios = [
            User(username="ana_silva",      password=generate_password_hash("123456"), user_type="Morador"),
            User(username="carlos_fonseca", password=generate_password_hash("123456"), user_type="Morador"),
            User(username="mariana_r",      password=generate_password_hash("123456"), user_type="Morador"),
            User(username="PetShopAmigos",  password=generate_password_hash("123456"), user_type="Parceiro"),
            User(username="MercadoBairro",  password=generate_password_hash("123456"), user_type="Parceiro"),
            User(username="joao_morador",   password=generate_password_hash("123456"), user_type="Morador"),
        ]
        for u in usuarios:
            db.session.add(u)
        db.session.commit()
        print(f"{len(usuarios)} usuarios criados. Senha de todos: 123456")

        ana      = User.query.filter_by(username="ana_silva").first()
        carlos   = User.query.filter_by(username="carlos_fonseca").first()
        mariana  = User.query.filter_by(username="mariana_r").first()
        petshop  = User.query.filter_by(username="PetShopAmigos").first()
        mercado  = User.query.filter_by(username="MercadoBairro").first()
        joao     = User.query.filter_by(username="joao_morador").first()

        agora = datetime.utcnow()

        # --- POSTS ---
        posts = [
            Post(
                content="ATENCAO MORADORES! Dois homens em moto preta foram vistos tentando arrombar o portão do condomínio Residencial das Flores por volta das 23h. Um deles usava boné vermelho. Já acionei a PM, mas fiquem alertas e reforcem os cadeados. Qualquer informação, avise no grupo de moradores.",
                category="Segurança",
                location="Rua das Acacias, prox. ao n 340",
                is_urgent=True,
                is_help=False,
                is_resolved=False,
                author=carlos,
                date_posted=agora - timedelta(hours=2),
            ),
            Post(
                content="Olá vizinhos! Minha mãe passou mal e precisamos de alguém que possa nos dar uma carona até o Hospital Regional hoje à tarde, por volta das 15h. Moramos na Rua Gustavo Zimermann, 89. Qualquer ajuda é muito bem-vinda.",
                category="Avisos",
                location="Rua Gustavo Zimermann, 89",
                is_urgent=False,
                is_help=True,
                is_resolved=False,
                author=mariana,
                date_posted=agora - timedelta(hours=5),
            ),
            Post(
                content="Pessoal, aquela vala aberta na calçada da Rua Pomerode que já causou algumas quedas foi finalmente tapada pela prefeitura! Obrigada a todos que assinaram o abaixo-assinado e ligaram para a ouvidoria. É isso que a mobilização comunitária faz!",
                category="Avisos",
                location="Rua Pomerode, altura do n 200",
                is_urgent=False,
                is_help=False,
                is_resolved=True,
                author=ana,
                date_posted=agora - timedelta(days=1),
            ),
            Post(
                content="PARA ADOCAO: Encontrei essa cachorrinha na rua ontem, aparentemente abandonada. Ela é dócil, obediente e se dá bem com crianças. Calculamos que tem uns 2 anos. Está vacinada e vermifugada. Quem puder dar um lar cheio de amor, entre em contato! Não consigo ficar com ela pois já tenho 3 cães.",
                category="Adoção",
                location="Vila Nova",
                is_urgent=False,
                is_help=False,
                is_resolved=False,
                author=ana,
                date_posted=agora - timedelta(days=2),
            ),
            Post(
                content="CAMPANHA DE ARRECADACAO - Igreja Batista do Bairro\n\nEstamos arrecadando roupas de inverno e alimentos nao-pereciveis para as famílias atingidas pelas chuvas no Vale do Itajaí. Pontos de coleta: Igreja Batista e Mercearia do Seu Antônio.",
                category="Doações",
                location="Igreja Batista - Rua 7 de Setembro",
                is_urgent=False,
                is_help=False,
                is_resolved=False,
                author=mariana,
                date_posted=agora - timedelta(days=3),
            ),
            Post(
                content="FESTA JUNINA DO BAIRRO - SAVE THE DATE!\n\nData: 21 de junho (sábado)\nHorário: 16h às 22h\nLocal: Praça Central\n\nTeremos quadrilha, comidas típicas, bingo e pescaria para as crianças. Entrada gratuita. Vamos celebrar juntos!",
                category="Eventos",
                location="Praca Central do Bairro",
                is_urgent=False,
                is_help=False,
                is_resolved=False,
                author=joao,
                date_posted=agora - timedelta(days=4),
            ),
            Post(
                content="Olá, comunidade! Somos o Pet Shop Amigos, aqui do bairro, e queremos fazer parte dessa rede de apoio! Neste mês oferecemos: Banho e tosa com 20% de desconto para moradores. Estamos na Rua Blumenau, 54.",
                category="Serviços",
                location="Rua Blumenau, 54",
                is_urgent=False,
                is_help=False,
                is_resolved=False,
                author=petshop,
                date_posted=agora - timedelta(days=5),
            ),
        ]

        for p in posts:
            db.session.add(p)
        db.session.commit()
        print(f"{len(posts)} posts criados.")

        post_adocao    = posts[3]
        post_arrecad   = posts[4]
        post_urgente   = posts[0]

        comentarios = [
            Comment(content="Que absurdo! Vou compartilhar no grupo dos moradores agora.", author=ana,     post=post_urgente,  date_posted=agora - timedelta(hours=1, minutes=45)),
            Comment(content="A PM passou aqui por volta da meia-noite, parece que afugentaram.", author=joao,    post=post_urgente,  date_posted=agora - timedelta(hours=1)),
            Comment(content="Que linda! Posso ir ver ela hoje à tarde?",                         author=mariana, post=post_adocao,   date_posted=agora - timedelta(days=1, hours=18)),
            Comment(content="Vou levar roupas de criança amanhã! Quantas sacolas posso levar?", author=carlos,  post=post_arrecad,  date_posted=agora - timedelta(days=2)),
        ]

        for c in comentarios:
            db.session.add(c)
        db.session.commit()
        print(f"{len(comentarios)} comentarios criados.")
        print("Seed concluido.")

if __name__ == "__main__":
    seed()