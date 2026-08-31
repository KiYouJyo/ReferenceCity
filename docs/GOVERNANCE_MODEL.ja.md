# ReferenceCity 計画ガバナンスモデル v0.1

> 日本語ミラー。中文: `GOVERNANCE_MODEL.md` · English: `GOVERNANCE_MODEL.en.md`

Phase 1C では、職務分離、機械判定可能な権限、監査可能な結果を持つ最小実験ガバナンスモデルを定義します。実在する行政機関の法定権限を完全に再現するものではありません。

6 つの役割を用います。PLANNER は草案作成・提出・変更開始、REVIEWER は審査・差戻し・拒否、APPROVER は承認・発効・旧版廃止、DISTRICT_MANAGER は指定区域のみのコントロール審査、APPLICANT は開発申請のみ、AUDITOR は Hash・バージョン・履歴の検証のみを行います。

標準ライフサイクルは DRAFT → SUBMITTED → REVIEWED → APPROVED → EFFECTIVE で、差戻し・拒否・撤回と EFFECTIVE → AMENDMENT → SUBMITTED の更新ループを含みます。各遷移には正しい現状態、許可された operation/role、必要文書・署名、バージョン前提条件、監査イベントが必要です。

本モデルは機能検証用の抽象モデルであり、中国の実際の法定手続と一対一対応するという主張ではありません。
