from data.data_penyakit import penyakit
from data.data_rules import rules

def forward_chaining(fakta, threshold=30):
    hasil = []

    for kd, syarat in rules.items():
        cocok = set(syarat) & fakta
        if not cocok:
            continue

        persentase = round(len(cocok) / len(syarat) * 100, 1)

        # Terapkan ambang batas (threshold)
        if persentase >= threshold:
            hasil.append({
                "kode": kd,
                "nama": penyakit[kd],
                "persentase": persentase,
                "jumlah_cocok": len(cocok),
                "total_gejala": len(syarat)
            })

    return sorted(hasil, key=lambda x: x["persentase"], reverse=True)
