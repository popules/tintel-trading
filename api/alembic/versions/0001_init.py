from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "ticker",
        sa.Column("symbol", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("exchange", sa.String(), nullable=False),
        sa.Column("sector", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("market_cap", sa.Float(), nullable=True),
        sa.Column("float", sa.Float(), nullable=True),
        sa.Column("adv20", sa.Float(), nullable=True),
        sa.Column("revenue_ttm", sa.Float(), nullable=True),
        sa.Column("ev_sales", sa.Float(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "dailymetrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(), sa.ForeignKey("ticker.symbol")),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("rsi14", sa.Float(), nullable=True),
        sa.Column("momentum_score", sa.Float(), nullable=True),
        sa.Column("quality_score", sa.Float(), nullable=True),
        sa.Column("catalysts_score", sa.Float(), nullable=True),
        sa.Column("valuation_score", sa.Float(), nullable=True),
        sa.Column("ai_score", sa.Float(), nullable=True),
        sa.Column("volume_z", sa.Float(), nullable=True),
    )
    op.create_table(
        "insider",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(), nullable=False, index=True),
        sa.Column("filed_at", sa.Date(), nullable=False),
        sa.Column("insider_name", sa.String(), nullable=False),
        sa.Column("shares", sa.Integer(), nullable=False),
        sa.Column("value_usd", sa.Float(), nullable=False),
        sa.Column("direction", sa.String(), nullable=False),
    )
    op.create_table(
        "offering",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(), nullable=False, index=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("amount_usd", sa.Float(), nullable=False),
    )
    op.create_table(
        "snapshot",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
    )

def downgrade():
    op.drop_table("snapshot")
    op.drop_table("offering")
    op.drop_table("insider")
    op.drop_table("dailymetrics")
    op.drop_table("ticker")
