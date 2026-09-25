# AI Core — интерактивная 3D-сцена (Blender + MCP)

🔗 **Смотреть в браузере:** https://eugene55555.github.io/git-blender/

Сцена, целиком сгенерированная программно: **Blender 5.0 в headless-режиме на сервере**, которым управлял агент (Hermes / Катя) через **MCP-протокол** — по той же схеме, что в AI-курсах про Blender MCP.

## Что внутри

| Путь | Что это |
|---|---|
| `index.html` | веб-просмотрщик на [model-viewer](https://modelviewer.dev) — крути сцену в браузере |
| `scene/ai_core.glb` | модель для веба (glTF 2.0, анимация `Orbit` — прецессия колец) |
| `scene/ai_core.blend` | исходник сцены для Blender |
| `scripts/ai_core_scene.py` | код, создавший сцену: сфера `AI_Core`, неоновые кольца, свет, камеры, настройки рендера |
| `scripts/anim_export.py` | анимация вращения колец + экспорт в glTF (GLB) |
| `scripts/send_blender.py` | как код доставляется в живой Blender по сокету (аддон «MCP for Blender», порт 9876) |
| `preview.png` | Cycles-рендер сцены (CPU, без GPU) |

## Как это было сделано

1. Blender 5.0.1 запущен headless (виртуальный дисплей Xvfb) на сервере.
2. К нему подключён MCP-аддон → агент может создавать объекты, материалы, свет, камеры, анимации и рендерить — командами.
3. Агент кодом (`bpy`) собрал сцену: тёмная глянцевая сфера + три орбитальных кольца (циан/magenta эмиссия), холодный и тёплый свет.
4. Экспорт в glTF → сайт для GitHub Pages.

## Локальный просмотр

```bash
git clone https://github.com/Eugene55555/git-blender
cd git-blender
python3 -m http.server 8000   # затем открыть http://localhost:8000
```
