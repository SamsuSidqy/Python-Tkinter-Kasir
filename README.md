## Tabel Barang
{
barang | CREATE TABLE `barang` (
  `id_barang` int(11) NOT NULL AUTO_INCREMENT,
  `kode_barang` varchar(200) NOT NULL,
  `nama_barang` varchar(200) NOT NULL,
  `harga` varchar(100) NOT NULL,
  `stok` int(10) NOT NULL,
  PRIMARY KEY (`id_barang`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
}

## Tabel Laporan
{
laporan | CREATE TABLE `laporan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kode_tranksaksi` varchar(255) NOT NULL,
  `data_barang` text NOT NULL,
  `total_belanja` varchar(200) NOT NULL,
  `total_tunai` varchar(200) NOT NULL,
  `total_kembalian` varchar(200) NOT NULL,
  `tanggal_tranksaksi` varchar(200) NOT NULL,
  `metode` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
}

## Tabel User
{
users | CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `kode_karyawan` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
}
