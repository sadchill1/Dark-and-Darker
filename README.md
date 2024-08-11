### ЦЕ НЕОФІЦІЙНА УКРАЇНСЬКА ЛОКАЛІЗАЦІЯ до гри [Dark and Darker](https://darkanddarker.com/).

Текст перекладено з англійської мови з допомогою ШІ та внесено ручні правки.

# Встановлення

1. Завантажити архів: https://github.com/sadchill1/Dark-and-Darker-UA/releases/latest/download/dark_and_darker_ua.zip
2. Файл `pakchunk0-Windows_0_P.pak` перемістити по шляху `Steam\steamapps\common\Dark and Darker\DungeonCrawler\Content\Paks\~mods`. Якщо папки `~mods` немає її потрібно створити. **ЗАМІНЯТИ ФАЙЛИ ГРИ НЕ ПОТРІБНО**
	* Якщо ви хочете, щоб були перекладені всі предмети в грі, то обирайте `.pak` з папки `ua`
	* Якщо ви хочете, щоб предмети мали оригінальні (англійські) назви, то обирайте `.pak` з папки `ua_no_items`
3. В грі обрати Англійську мову.

# Для тих, хто хоче допомогти з перекладом

Робіть [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) цього репозиторію та створюйте [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) зі своїми правками.

Гра використовує файли локалізації у форматі `*.locres`. Для зручності в репозиторії ці файли зберігаються у форматі `*.csv` в папці `data`.

`./data/!base.csv` це файл зі всіма ключами та оригінальною (англійською) локалізацією станом на останній патч гри. Цей файл використовується як еталон і його змінювати не потрібно. Всі решта `*.csv` файли також включають в собі і українську локалізацію. Саме в ці файли і потрібно вносити правки.

`*.csv` файли мають формат `<ключ>,<оригінал>,<переклад>`

# Для тих, хто хоче допомогти з підтримкою цього репозиторію

`UE4localizationsTool.exe` це утиліта яка дозволяє переглядати та модифікувати бінарні `*.locres` файли локалізації.

[`UnrealLocres.exe`](https://github.com/akintos/UnrealLocres) утиліта яка дозволяє перетворювати `*.locres` файли у `*.csv`, а також пропатчувати `*.locres` файли з українською локалізацією.

`Game.locres` це файл з оригінальною (англійською) локалізацією поверх якого накладається українська локалізація.

`main.py` це основний скрипт за допомогою якого оновлюється `Game.locres` при виході нового патчу. Також цей скрипт обробляє всі `*.csv` файли та створює пропатчений `*.locres` з українською локалізацією.

Приклад:
```cmd
python.exe main.py --help
python.exe main.py migrate --source .\Game_new.locres  # оновити Game.locres
python.exe main.py patch  # створити *.locres з українською локалізацією
```

***

Якщо у вас залишились питання чи виникли проблеми із встановленням, заходьте до [нашого Діскорд каналу](https://discord.gg/u6M9bN2yYX).
