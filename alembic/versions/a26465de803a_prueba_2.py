"""prueba 2

Revision ID: a26465de803a
Revises: db35a3183a0f
Create Date: 2025-10-06 19:56:13.690674
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = 'a26465de803a'
down_revision: Union[str, Sequence[str], None] = 'db35a3183a0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1️⃣ Crear primero User
    op.create_table(
        'User',
        sa.Column('id_user', sa.UUID(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('rol_user', sa.String(length=60), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('id_usuario_creacion', sa.UUID(), nullable=True),
        sa.Column('id_usuario_actualizacion', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['id_usuario_actualizacion'], ['User.id_user']),
        sa.ForeignKeyConstraint(['id_usuario_creacion'], ['User.id_user']),
        sa.PrimaryKeyConstraint('id_user'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )

    # 2️⃣ User_Information
    op.create_table(
        'User_Information',
        sa.Column('id_user_information', sa.UUID(), nullable=False),
        sa.Column('first_name_user', sa.String(length=50), nullable=False),
        sa.Column('second_name_user', sa.String(length=50), nullable=True),
        sa.Column('first_lastname_user', sa.String(length=50), nullable=False),
        sa.Column('second_lastname_user', sa.String(length=50), nullable=True),
        sa.Column('birth_date_user', sa.Date(), nullable=False),
        sa.Column('gender_user', sa.String(length=50), nullable=False),
        sa.Column('phone_number_user', sa.String(length=20), nullable=False),
        sa.Column('document_number_user', sa.String(length=30), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('update_date', sa.DateTime(timezone=True)),
        sa.Column('id_user_create', sa.UUID(), nullable=False),
        sa.Column('id_user_update', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['id_user_create'], ['User.id_user']),
        sa.ForeignKeyConstraint(['id_user_update'], ['User.id_user']),
        sa.ForeignKeyConstraint(['user_id'], ['User.id_user']),
        sa.PrimaryKeyConstraint('id_user_information'),
    )

    # 3️⃣ Medic, Nurse y Patient
    op.create_table(
        'Medic',
        sa.Column('id_medic', sa.UUID(), nullable=False),
        sa.Column('speciality', sa.String(length=50), nullable=False),
        sa.Column('id_information', sa.UUID(), nullable=True),
        sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('update_date', sa.DateTime(timezone=True)),
        sa.Column('id_user_create', sa.UUID(), nullable=False),
        sa.Column('id_user_update', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['id_information'], ['User_Information.id_user_information']),
        sa.ForeignKeyConstraint(['id_user_create'], ['User.id_user']),
        sa.ForeignKeyConstraint(['id_user_update'], ['User.id_user']),
        sa.PrimaryKeyConstraint('id_medic'),
    )

    op.create_table(
        'Nurse',
        sa.Column('id_nurse', sa.UUID(), nullable=False),
        sa.Column('salary', sa.Float(precision=15, asdecimal=2), nullable=False),
        sa.Column('speciality', sa.String(length=50), nullable=False),
        sa.Column('id_information', sa.UUID(), nullable=True),
        sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('update_date', sa.DateTime(timezone=True)),
        sa.Column('id_user_create', sa.UUID(), nullable=False),
        sa.Column('id_user_update', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['id_information'], ['User_Information.id_user_information']),
        sa.ForeignKeyConstraint(['id_user_create'], ['User.id_user']),
        sa.ForeignKeyConstraint(['id_user_update'], ['User.id_user']),
        sa.PrimaryKeyConstraint('id_nurse'),
    )

    op.create_table(
        'Patient',
        sa.Column('id_patient', sa.UUID(), nullable=False),
        sa.Column('id_information', sa.UUID(), nullable=True),
        sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('update_date', sa.DateTime(timezone=True)),
        sa.Column('id_user_create', sa.UUID(), nullable=False),
        sa.Column('id_user_update', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['id_information'], ['User_Information.id_user_information']),
        sa.ForeignKeyConstraint(['id_user_create'], ['User.id_user']),
        sa.ForeignKeyConstraint(['id_user_update'], ['User.id_user']),
        sa.PrimaryKeyConstraint('id_patient'),
    )

    # 4️⃣ Diagnosis (sin FK a Medical_Appointment)
    op.create_table(
        'Diagnosis',
        sa.Column('id_diagnosis', sa.UUID(), nullable=False),
        sa.Column('diagnosis_date', sa.Date(), nullable=False),
        sa.Column('diagnosis_description', sa.String(length=255), nullable=False),
        sa.Column('id_medical_appointment', sa.UUID(), nullable=True),
        sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('update_date', sa.DateTime(timezone=True)),
        sa.Column('id_user_create', sa.UUID(), nullable=False),
        sa.Column('id_user_update', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['id_user_create'], ['User.id_user']),
        sa.ForeignKeyConstraint(['id_user_update'], ['User.id_user']),
        sa.PrimaryKeyConstraint('id_diagnosis'),
    )

    # 5️⃣ Medical_Appointment (sin FK a Diagnosis)
    op.create_table(
        'Medical_Appointment',
        sa.Column('id_medical_appointment', sa.UUID(), nullable=False),
        sa.Column('appointment_date', sa.Date(), nullable=False),
        sa.Column('appointment_hour', sa.Time(), nullable=False),
        sa.Column('location', sa.String(length=100), nullable=False),
        sa.Column('id_medic', sa.UUID(), nullable=True),
        sa.Column('id_nurse', sa.UUID(), nullable=True),
        sa.Column('id_patient', sa.UUID(), nullable=True),
        sa.Column('id_diagnosis', sa.UUID(), nullable=True),
        sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('update_date', sa.DateTime(timezone=True)),
        sa.Column('id_user_create', sa.UUID(), nullable=False),
        sa.Column('id_user_update', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['id_medic'], ['Medic.id_medic']),
        sa.ForeignKeyConstraint(['id_nurse'], ['Nurse.id_nurse']),
        sa.ForeignKeyConstraint(['id_patient'], ['Patient.id_patient']),
        sa.ForeignKeyConstraint(['id_user_create'], ['User.id_user']),
        sa.ForeignKeyConstraint(['id_user_update'], ['User.id_user']),
        sa.PrimaryKeyConstraint('id_medical_appointment'),
    )

    # 6️⃣ Bill
    op.create_table(
        'Bill',
        sa.Column('id_bill', sa.UUID(), nullable=False),
        sa.Column('generation_date', sa.Date(), nullable=False),
        sa.Column('generation_hour', sa.Time(), nullable=False),
        sa.Column('total', sa.Float(precision=10, asdecimal=2), nullable=False),
        sa.Column('id_patient', sa.UUID(), nullable=True),
        sa.Column('id_medical_appointment', sa.UUID(), nullable=True),
        sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('update_date', sa.DateTime(timezone=True)),
        sa.Column('id_user_create', sa.UUID(), nullable=False),
        sa.Column('id_user_update', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['id_medical_appointment'], ['Medical_Appointment.id_medical_appointment']),
        sa.ForeignKeyConstraint(['id_patient'], ['Patient.id_patient']),
        sa.ForeignKeyConstraint(['id_user_create'], ['User.id_user']),
        sa.ForeignKeyConstraint(['id_user_update'], ['User.id_user']),
        sa.PrimaryKeyConstraint('id_bill'),
    )

    # 7️⃣ Ahora sí: crear las FKs cruzadas (una vez ambas tablas existen)
    op.create_foreign_key(
        'fk_diagnosis_medicalappointment',
        'Diagnosis', 'Medical_Appointment',
        ['id_medical_appointment'], ['id_medical_appointment']
    )
    op.create_foreign_key(
        'fk_medicalappointment_diagnosis',
        'Medical_Appointment', 'Diagnosis',
        ['id_diagnosis'], ['id_diagnosis']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_medicalappointment_diagnosis', 'Medical_Appointment', type_='foreignkey')
    op.drop_constraint('fk_diagnosis_medicalappointment', 'Diagnosis', type_='foreignkey')
    op.drop_table('Bill')
    op.drop_table('Medical_Appointment')
    op.drop_table('Diagnosis')
    op.drop_table('Patient')
    op.drop_table('Nurse')
    op.drop_table('Medic')
    op.drop_table('User_Information')
    op.drop_table('User')
