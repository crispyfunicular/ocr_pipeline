import os
import json
import jiwer
import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def extraire_texte(chemin_fichier, langue):
    textes = []
    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                if ligne.strip():
                    donnees = json.loads(ligne)
                    if langue in donnees:
                        textes.append(donnees[langue])
    return " ".join(textes)


def evaluer_manuel(nom_manuel):
    # Les chemins sont relatifs à la racine du projet
    dossier_ref = PROJECT_ROOT / "error_rates" / nom_manuel / "human_reference"
    dossier_hyp = PROJECT_ROOT / "error_rates" / nom_manuel / "jsonl"

    if not dossier_ref.exists():
        print(f"⚠️ Dossier de référence introuvable pour {nom_manuel}", file=sys.stderr)
        return False

    print(f"\n=== ÉVALUATION : {nom_manuel} ===")

    for fichier in sorted(os.listdir(dossier_ref)):
        if fichier.endswith(".jsonl"):
            chemin_ref = dossier_ref / fichier
            chemin_hyp = dossier_hyp / fichier

            if not chemin_hyp.exists():
                print(
                    f"⚠️ Fichier hypothèse introuvable : {chemin_hyp.name}",
                    file=sys.stderr,
                )
                continue

            ref_br = extraire_texte(chemin_ref, "breton")
            hyp_br = extraire_texte(chemin_hyp, "breton")

            ref_fr = extraire_texte(chemin_ref, "français")
            hyp_fr = extraire_texte(chemin_hyp, "français")

            print(f"📄 {fichier} :")
            if ref_br and hyp_br:
                try:
                    wer_br = jiwer.wer(ref_br, hyp_br) * 100
                except Exception:
                    wer_br = None
                
                try:
                    cer_br = jiwer.cer(ref_br, hyp_br) * 100
                except Exception:
                    cer_br = None

                if wer_br is not None and cer_br is not None:
                    print(f"  Breton   -> WER: {wer_br:.1f}%, CER: {cer_br:.1f}%")
                elif wer_br is not None:
                    print(f"  Breton   -> WER: {wer_br:.1f}%")
                else:
                    print(f"  Breton   -> Impossible de calculer WER/CER")

            if ref_fr and hyp_fr:
                try:
                    wer_fr = jiwer.wer(ref_fr, hyp_fr) * 100
                except Exception:
                    wer_fr = None
                    
                try:
                    cer_fr = jiwer.cer(ref_fr, hyp_fr) * 100
                except Exception:
                    cer_fr = None
                
                if wer_fr is not None and cer_fr is not None:
                    print(f"  Français -> WER: {wer_fr:.1f}%, CER: {cer_fr:.1f}%")
                elif wer_fr is not None:
                    print(f"  Français -> WER: {wer_fr:.1f}%")
                else:
                    print(f"  Français -> Impossible de calculer WER/CER")

    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description="Évaluation du WER et CER")
    parser.add_argument(
        "targets",
        nargs="*",
        help="Noms des manuels (défaut: tous dans error_rates)",
    )
    args = parser.parse_args(argv)

    if args.targets:
        manuels_a_evaluer = args.targets
    else:
        error_rates_dir = PROJECT_ROOT / "error_rates"
        if error_rates_dir.exists():
            manuels_a_evaluer = [
                d.name for d in error_rates_dir.iterdir() if d.is_dir()
            ]
        else:
            print(f"❌ Dossier {error_rates_dir} introuvable.", file=sys.stderr)
            return 1

    success = True
    for manuel in sorted(manuels_a_evaluer):
        if not evaluer_manuel(manuel):
            success = False

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())