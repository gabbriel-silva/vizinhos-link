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

        # Limpa dados antigos (opcional — comente se não quiser apagar)
        Comment.query.delete()
        Post.query.delete()
        User.query.delete()
        db.session.commit()
        print("🗑️  Banco limpo.")

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
        print(f"✅ {len(usuarios)} usuários criados. Senha de todos: 123456")

        ana      = User.query.filter_by(username="ana_silva").first()
        carlos   = User.query.filter_by(username="carlos_fonseca").first()
        mariana  = User.query.filter_by(username="mariana_r").first()
        petshop  = User.query.filter_by(username="PetShopAmigos").first()
        mercado  = User.query.filter_by(username="MercadoBairro").first()
        joao     = User.query.filter_by(username="joao_morador").first()

        agora = datetime.utcnow()

        # --- POSTS ---
        posts = [
            # 🚨 URGENTE
            Post(
                content="⚠️ ATENÇÃO MORADORES! Dois homens em moto preta foram vistos tentando arrombar o portão do condomínio Residencial das Flores por volta das 23h. Um deles usava boné vermelho. Já acionei a PM, mas fiquem alertas e reforcem os cadeados. Qualquer informação, avise no grupo do WhatsApp.",
                category="Segurança",
                location="Rua das Acácias, próx. ao nº 340",
                is_urgent=True,
                is_help=False,
                is_resolved=False,
                author=carlos,
                date_posted=agora - timedelta(hours=2),
            ),
            # 🆘 PEDIDO DE AJUDA
            Post(
                content="Olá vizinhos! Minha mãe passou mal e precisamos de alguém que possa nos dar uma carona até o Hospital Regional hoje à tarde, por volta das 15h. Moramos na Rua Gustavo Zimermann, 89. Qualquer ajuda é muito bem-vinda. 🙏",
                category="Avisos",
                location="Rua Gustavo Zimermann, 89",
                is_urgent=False,
                is_help=True,
                is_resolved=False,
                author=mariana,
                date_posted=agora - timedelta(hours=5),
            ),
            # ✅ PROBLEMA RESOLVIDO
            Post(
                content="Pessoal, aquela vala aberta na calçada da Rua Pomerode que já causou algumas quedas foi finalmente tapada pela prefeitura! Obrigada a todos que assinaram o abaixo-assinado e ligaram para a ouvidoria. É isso que a mobilização comunitária faz! 💪",
                category="Avisos",
                location="Rua Pomerode, altura do nº 200",
                is_urgent=False,
                is_help=False,
                is_resolved=True,
                author=ana,
                date_posted=agora - timedelta(days=1),
            ),
            # 🐾 ADOÇÃO
            Post(
                content="🐕 PARA ADOÇÃO: Encontrei essa cachorrinha na rua ontem, aparentemente abandonada. Ela é dócil, obediente e se dá bem com crianças. Calculamos que tem uns 2 anos. Está vacinada e vermifugada (já levei ao vet). Quem puder dar um lar cheio de amor, entre em contato! Não consigo ficar com ela pois já tenho 3 cães.",
                category="Adoção",
                location="Vila Nova",
                is_urgent=False,
                is_help=False,
                is_resolved=False,
                author=ana,
                date_posted=agora - timedelta(days=2),
            ),
            # 🤝 ARRECADAÇÃO
            Post(
                content="🤝 CAMPANHA DE ARRECADAÇÃO — Igreja Batista do Bairro\n\nEstamos arrecadando roupas de inverno (adulto e infantil) e alimentos não-perecíveis para as famílias atingidas pelas chuvas no Vale do Itajaí. \n\nPontos de coleta:\n📍 Igreja Batista — Rua 7 de Setembro, 410\n📍 Mercearia do Seu Antônio — Rua das Palmeiras\n\nCampanha vai até dia 30. Cada doação faz diferença! ❤️",
                category="Doações",
                location="Igreja Batista — Rua 7 de Setembro",
                is_urgent=False,
                is_help=False,
                is_resolved=False,
                author=mariana,
                date_posted=agora - timedelta(days=3),
            ),
            # 🎉 EVENTO
            Post(
                content="🎉 FESTA JUNINA DO BAIRRO — SAVE THE DATE!\n\nData: 21 de junho (sábado)\nHorário: 16h às 22h\nLocal: Praça Central\n\nTeremos quadrilha, comidas típicas, bingo, pescaria para as crianças e muito forró! Entrada gratuita. Vamos celebrar juntos e fortalecer nossa comunidade! 🎶🌽",
                category="Eventos",
                location="Praça Central do Bairro",
                is_urgent=False,
                is_help=False,
                is_resolved=False,
                author=joao,
                date_posted=agora - timedelta(days=4),
            ),
            # 🛠️ PARCEIRO LOCAL
            Post(
                content="🏬 Olá, comunidade! Somos o Pet Shop Amigos, aqui do bairro, e queremos fazer parte dessa rede de apoio!\n\nNeste mês oferecemos:\n✂️ Banho e tosa com 20% de desconto para moradores\n💉 Vacinação antirrábica gratuita todo 1º sábado do mês\n🐾 Recebemos doações de ração para animais em situação de rua\n\nEstamos na Rua Blumenau, 54. Sigam nas redes: @petshopamigos 🐶🐱",
                category="Serviços",
                location="Rua Blumenau, 54",
                is_urgent=False,
                is_help=False,
                is_resolved=False,
                author=petshop,
                date_posted=agora - timedelta(days=5),
            ),
            # 🛒 PARCEIRO — MERCADO
            Post(
                content="📣 Mercado do Bairro informa: toda sexta-feira a partir das 17h temos o Sacolão Solidário — frutas, legumes e verduras por preços populares. Além disso, aceitamos doações de alimentos para redistribuir a famílias em vulnerabilidade cadastradas na associação de moradores. Contamos com vocês! 🥦🍎",
                category="Serviços",
                location="Av. Principal, 120",
                is_urgent=False,
                is_help=False,
                is_resolved=False,
                author=mercado,
                date_posted=agora - timedelta(days=6),
            ),
            # 📢 AVISO GERAL
            Post(
                content="Atenção moradores da quadra 4! O caminhão de coleta de lixo eletrônico (TVs, geladeiras, computadores, baterias) passará na nossa rua na próxima terça-feira, dia 27, entre 8h e 12h. Deixem os itens na calçada até as 7h30. Aproveitem para fazer o descarte correto! ♻️",
                category="Avisos",
                location="Quadra 4 — Rua das Palmeiras",
                is_urgent=False,
                is_help=False,
                is_resolved=False,
                author=joao,
                date_posted=agora - timedelta(days=7),
            ),
            # 🔴 URGENTE RESOLVIDO
            Post(
                content="RESOLVIDO ✅ — O vazamento de água que estava inundando a calçada da Rua Itajaí foi corrigido pela SAMAE hoje de manhã. Obrigado a todos que reportaram e à equipe que atendeu rápido! Caso percebam algum resíduo de água ainda escorregando, avisem novamente.",
                category="Avisos",
                location="Rua Itajaí, 88",
                is_urgent=False,
                is_help=False,
                is_resolved=True,
                author=carlos,
                date_posted=agora - timedelta(days=8),
            ),
        ]

        for p in posts:
            db.session.add(p)
        db.session.commit()
        print(f"✅ {len(posts)} posts criados.")

        # --- COMENTÁRIOS ---
        post_adocao    = posts[3]
        post_arrecad   = posts[4]
        post_evento    = posts[5]
        post_urgente   = posts[0]

        comentarios = [
            Comment(content="Que absurdo! Vou compartilhar no grupo dos moradores agora.", author=ana,     post=post_urgente,  date_posted=agora - timedelta(hours=1, minutes=45)),
            Comment(content="A PM passou aqui por volta da meia-noite, parece que afugentaram.", author=joao,    post=post_urgente,  date_posted=agora - timedelta(hours=1)),
            Comment(content="Que gatinha linda! 😍 Posso ir ver ela hoje à tarde?",             author=mariana, post=post_adocao,   date_posted=agora - timedelta(days=1, hours=18)),
            Comment(content="Também tenho interesse! Me manda mensagem.",                        author=joao,    post=post_adocao,   date_posted=agora - timedelta(days=1, hours=10)),
            Comment(content="Vou levar roupas de criança amanhã! Quantas sacolas posso levar?", author=carlos,  post=post_arrecad,  date_posted=agora - timedelta(days=2)),
            Comment(content="Passarei lá na sexta com algumas latas de leite em pó. 🙏",         author=ana,     post=post_arrecad,  date_posted=agora - timedelta(days=2, hours=6)),
            Comment(content="Já está no calendário! Vou levar o pessoal todo. 🎉",              author=mariana, post=post_evento,   date_posted=agora - timedelta(days=3)),
        ]

        for c in comentarios:
            db.session.add(c)
        db.session.commit()
        print(f"✅ {len(comentarios)} comentários criados.")

        print("\n🎉 Seed concluído com sucesso!")
        print("=" * 45)
        print("Usuários para login (senha: 123456):")
        for u in usuarios:
            print(f"  • {u.username} ({u.user_type})")
        print("=" * 45)
        print("Acesse: http://127.0.0.1:5000")

if __name__ == "__main__":
    seed()