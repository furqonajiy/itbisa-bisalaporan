import logging

from keywordchecker.generic import handle_invalid_keywords

VALID_TRANSAKSI_KEYWORD = [
    # V1

    # V2

    # V3
    'Belum Bayar',
    'Perlu Dikirim',
    'Sedang Dikirim',
    'Telah Dikirim',
    'Selesai',
    'Batal',
    'Pesanan diterima, namun Pembeli masih dapat mengajukan pengembalian hingga '
]

VALID_NOMINAL_REMIT_KEYWORD = [
    # Nominal Remit
    'Penghasilan dari Pesanan',
    'Kompensasi kehilangan',
    'Penyesuaian untuk',
    'Penggantian Dana Sebagian Barang Hilang',
    'Auto-approve compensation without judging',
    'SPinjam untuk Penjual'
]

VALID_KEUNTUNGAN_TAMBAHAN_KEYWORD = [
    # Keuntungan Tambahan
    'Penggantian Dana Penuh'
]

VALID_KERUGIAN_TAMBAHAN_KEYWORD = [
    # Kerugian Tambahan
    'Penyesuaian Saldo Penjual Karena Kekurangan Ongkir Pengembalian'
]

VALID_BONUS_KEYWORD = [
    # BisaBonus
    'Cashback JNE'
]

VALID_SALDO_KEYWORD = [
    # Not Used
    'Penarikan Dana',
    'Shopee Ongkir',
    'Pengembalian Dana untuk Penarikan Gagal',
] + VALID_NOMINAL_REMIT_KEYWORD + VALID_KEUNTUNGAN_TAMBAHAN_KEYWORD + VALID_KERUGIAN_TAMBAHAN_KEYWORD + VALID_BONUS_KEYWORD

def check_saldo_keyword(shp_file, df):
    logging.debug("Check BisaSaldo Keyword in {0}".format(shp_file))

    invalid_rows = df[~df['Deskripsi'].str.contains('|'.join(VALID_SALDO_KEYWORD))]

    handle_invalid_keywords('BisaSaldo', shp_file, invalid_rows)


def check_status_keyword(version, shp_file, df):
    logging.info("Check BisaTransaksi Keyword in {0}".format(shp_file))

    if version == "1":
        invalid_rows = df[~df['Order Status'].isin(VALID_TRANSAKSI_KEYWORD)]
    elif version == "2":
        invalid_rows = df[~df['Status Pesanan'].isin(VALID_TRANSAKSI_KEYWORD)]
    elif version == "3":
        df['Status Pesanan'] = df['Status Pesanan'].str.replace(
            r'(Pesanan diterima, namun Pembeli masih dapat mengajukan pengembalian hingga )\d{4}-\d{2}-\d{2}\.',
            r'\1',
            regex=True
        )
        invalid_rows = df[~df['Status Pesanan'].isin(VALID_TRANSAKSI_KEYWORD)]

    handle_invalid_keywords('BisaTransaksi', shp_file, invalid_rows)
