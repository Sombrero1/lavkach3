"""initial

Revision ID: d873f8f48b14
Revises: 
Create Date: 2023-06-07 14:54:46.176550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd873f8f48b14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('lsn', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.Unicode(length=255), nullable=False),
    sa.Column('external_id', sa.Unicode(length=255), nullable=True),
    sa.Column('lang', sa.Unicode(length=255), nullable=False),
    sa.Column('country', sa.Unicode(length=255), nullable=False),
    sa.Column('currency', sa.Unicode(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('external_id')
    )
    op.create_index(op.f('ix_companies_id'), 'companies', ['id'], unique=False)
    op.create_index(op.f('ix_companies_lsn'), 'companies', ['lsn'], unique=False)
    op.create_table('stores',
    sa.Column('lsn', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.Unicode(length=255), nullable=False),
    sa.Column('external_id', sa.Unicode(length=255), nullable=True),
    sa.Column('address', sa.Unicode(length=255), nullable=False),
    sa.Column('source', sa.Unicode(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('external_id')
    )
    op.create_index(op.f('ix_stores_id'), 'stores', ['id'], unique=False)
    op.create_index(op.f('ix_stores_lsn'), 'stores', ['lsn'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('password', sa.Unicode(length=255), nullable=False),
    sa.Column('email', sa.Unicode(length=255), nullable=False),
    sa.Column('nickname', sa.Unicode(length=255), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('company_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('nickname')
    )
    op.create_index(op.f('ix_users_company_id'), 'users', ['company_id'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###
    op.execute("create sequence companies_lsn_seq")
    op.execute("create sequence stores_lsn_seq")

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_company_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_stores_lsn'), table_name='stores')
    op.drop_index(op.f('ix_stores_id'), table_name='stores')
    op.drop_table('stores')
    op.drop_index(op.f('ix_companies_lsn'), table_name='companies')
    op.drop_index(op.f('ix_companies_id'), table_name='companies')
    op.drop_table('companies')
    # ### end Alembic commands ###
    op.execute("drop sequence companies_lsn_seq")
    op.execute("drop sequence stores_lsn_seq")