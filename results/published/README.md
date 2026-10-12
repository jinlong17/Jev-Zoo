# Lab draft result summaries

These sanitized files are release candidates. Public publication requires approval of their exact bundle.

Smoke verifies integration only. Full results below cover **JevBench public 231 records only**, without sealed/composite score.
Models have different native prompts/readouts/calibration contracts; see each summary protocol.
Timing includes cold kernels and is not a controlled latency ranking. No commercial API was called.

| Model | Attempted / eligible | Errors | Micro argmax agreement including errors | Official family macro accuracy | Brier | NLL |
|---|---|---|---|---|---|---|
| clef | 231/231 | 0 | 0.8744588744588745 | 0.880390314020345 | 0.16688203565111048 | 0.30949094817340234 |
| clef-flash | 231/231 | 0 | 0.8268398268398268 | 0.8289615651328757 | 0.23545077752479454 | 0.4215721500374777 |
| h2o-lightning-4b | 231/231 | 0 | 0.8831168831168831 | 0.9013542844038199 | 0.16397523140400622 | 0.3405053915233784 |
| imajev-2b | 231/231 | 0 | 0.7748917748917749 | 0.7676757935142868 | 0.30414884777432966 | 0.545446688018426 |
| imajev-4b | 231/231 | 0 | 0.8614718614718615 | 0.8698582649434043 | 0.18701871670779754 | 0.32719686895536026 |
| onejev-08b | 231/231 | 0 | 0.7012987012987013 | 0.7086927558547785 | 0.38255398534311685 | 0.6667247154194643 |
| onejev-4b | 231/231 | 0 | 0.7402597402597403 | 0.7477765082641243 | 0.3191456915465065 | 0.5479150052911074 |
| pplx-decider-27b | 231/231 | 0 | 0.8701298701298701 | 0.8891019760730803 | 0.15460618169739174 | 0.2741763464288881 |
| qwen35-2b | 231/231 | 0 | 0.6666666666666666 | 0.6669476660059735 | 0.4452629500189405 | 0.8101518166834013 |
| qwen35-4b | 231/231 | 0 | 0.7272727272727273 | 0.7428219923446961 | 0.34148767583367723 | 0.5969112531949997 |
