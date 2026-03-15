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
    dossier_ref = PROJECT_ROOT / "review" / nom_manuel
    dossier_hyp = PROJECT_ROOT / "ocr" / nom_manuel / "antigravity"

    if not dossier_ref.exists():
        print(f"⚠️ Dossier de référence introuvable pour {nom_manuel}", file=sys.stderr)
        return False

    print(f"\n=== ÉVALUATION : {nom_manuel} ===")

    report_lines = []
    header_lines = []
    header_lines.append(f"# Rapport d'erreur OCR : {nom_manuel}")
    header_lines.append(f"**Référence** : `review/{nom_manuel}`")
    header_lines.append(f"**Hypothèse** : `ocr/{nom_manuel}/antigravity`")
    header_lines.append("")

    detailed_lines = []
    detailed_lines.append("## Résultats détaillés par page")
    detailed_lines.append("")

    all_ref_br = []
    all_hyp_br = []
    all_ref_fr = []
    all_hyp_fr = []

    for fichier in sorted(os.listdir(dossier_ref)):
        if fichier.endswith(".jsonl"):
            chemin_ref = dossier_ref / fichier
            chemin_hyp = dossier_hyp / fichier

            if not chemin_hyp.exists():
                msg = f"⚠️ Fichier hypothèse introuvable : {chemin_hyp.name}"
                print(msg, file=sys.stderr)
                detailed_lines.append(msg)
                detailed_lines.append("")
                continue

            ref_br = extraire_texte(chemin_ref, "breton")
            hyp_br = extraire_texte(chemin_hyp, "breton")

            ref_fr = extraire_texte(chemin_ref, "français")
            hyp_fr = extraire_texte(chemin_hyp, "français")

            if ref_br and hyp_br:
                all_ref_br.append(ref_br)
                all_hyp_br.append(hyp_br)

            if ref_fr and hyp_fr:
                all_ref_fr.append(ref_fr)
                all_hyp_fr.append(hyp_fr)

            print(f"📄 {fichier} :")
            detailed_lines.append(f"### {fichier}")

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
                    msg = f"  Breton   -> WER: {wer_br:.1f}%, CER: {cer_br:.1f}%"
                elif wer_br is not None:
                    msg = f"  Breton   -> WER: {wer_br:.1f}%"
                else:
                    msg = f"  Breton   -> Impossible de calculer WER/CER"
                print(msg)
                detailed_lines.append(
                    f"- **Breton** : {msg.replace('  Breton   -> ', '')}"
                )

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
                    msg = f"  Français -> WER: {wer_fr:.1f}%, CER: {cer_fr:.1f}%"
                elif wer_fr is not None:
                    msg = f"  Français -> WER: {wer_fr:.1f}%"
                else:
                    msg = f"  Français -> Impossible de calculer WER/CER"
                print(msg)
                detailed_lines.append(
                    f"- **Français** : {msg.replace('  Français -> ', '')}"
                )

            detailed_lines.append("")

    print(f"\n--- RÉSULTAT GLOBAL : {nom_manuel} ---")
    global_lines = []
    global_lines.append("## Résultats Globaux")
    global_lines.append("")

    global_ref_br = " ".join(all_ref_br)
    global_hyp_br = " ".join(all_hyp_br)

    if global_ref_br and global_hyp_br:
        try:
            g_wer_br = jiwer.wer(global_ref_br, global_hyp_br) * 100
            g_cer_br = jiwer.cer(global_ref_br, global_hyp_br) * 100
            msg = f"🌐 Breton   GLOBAL -> WER: {g_wer_br:.1f}%, CER: {g_cer_br:.1f}%"
            print(msg)
            global_lines.append(
                f"- **Breton GLOBAL** : WER: **{g_wer_br:.1f}%**, CER: **{g_cer_br:.1f}%**"
            )
        except Exception as e:
            msg = f"🌐 Breton   GLOBAL -> Erreur de calcul : {e}"
            print(msg)
            global_lines.append(f"- **Breton GLOBAL** : *Erreur de calcul*")

    global_ref_fr = " ".join(all_ref_fr)
    global_hyp_fr = " ".join(all_hyp_fr)

    if global_ref_fr and global_hyp_fr:
        try:
            g_wer_fr = jiwer.wer(global_ref_fr, global_hyp_fr) * 100
            g_cer_fr = jiwer.cer(global_ref_fr, global_hyp_fr) * 100
            msg = f"🌐 Français GLOBAL -> WER: {g_wer_fr:.1f}%, CER: {g_cer_fr:.1f}%"
            print(msg)
            global_lines.append(
                f"- **Français GLOBAL** : WER: **{g_wer_fr:.1f}%**, CER: **{g_cer_fr:.1f}%**"
            )
        except Exception as e:
            msg = f"🌐 Français GLOBAL -> Erreur de calcul : {e}"
            print(msg)
            global_lines.append(f"- **Français GLOBAL** : *Erreur de calcul*")

    print("")
    global_lines.append("")

    # Assemblage du rapport: en-tête, global, puis détaillé
    report_lines = header_lines + global_lines + detailed_lines

    # Save the report to error_rates/{nom_manuel}/report.md
    output_dir = PROJECT_ROOT / "error_rates" / nom_manuel
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "report.md"
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        print(f"✅ Rapport sauvegardé dans {report_path.relative_to(PROJECT_ROOT)}")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde du rapport : {e}", file=sys.stderr)

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
        review_dir = PROJECT_ROOT / "review"
        if review_dir.exists():
            manuels_a_evaluer = [d.name for d in review_dir.iterdir() if d.is_dir()]
        else:
            print(f"❌ Dossier {review_dir} introuvable.", file=sys.stderr)
            return 1

    success = True
    for manuel in sorted(manuels_a_evaluer):
        if not evaluer_manuel(manuel):
            success = False

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
