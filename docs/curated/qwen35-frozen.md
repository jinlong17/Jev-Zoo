# Qwen3.5 frozen baseline

固定同一个instruction/base checkpoint；两者不能随意混配对照。

- id: `qwen35-frozen`
- name: `Qwen3.5 frozen baseline`
- kind: `baseline_model`
- parameter_scale_label: `2B primary / 4B comparison`
- modalities_declared: `['text', 'image', 'video']`
- modalities_locally_verified: `[]`
- upstream_availability: `public_backbone`
- recommended_role: `同骨干未训练对照`
- priority: `P0`
- training_access: `frozen_then_lora`
- license_review: `component_review_required`
- evidence_status: `source_reviewed`
- verified_on: `2026-10-06`
- revision: `None`
- adapter_implemented: `False`
- smoke_tested: `False`
- benchmark_reproduced: `False`
- enable_paid_by_default: `False`

- Source: https://huggingface.co/Qwen/Qwen3.5-2B
- Source: https://huggingface.co/Qwen/Qwen3.5-4B

Seed metadata dated 2026-10-06 remains historical; real execution evidence is maintained in the checkpoint cards and approved summaries.
