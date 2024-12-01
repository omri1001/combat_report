# grades.py

from telegram.ext import ConversationHandler

# Define the grading structure
parts = {
    "פיקוד ושליטה": {
        "1.1 גיבוש תמונת מצב": None,
        "1.2 ניהול הכוח, חלוקת גזרות, הזרמת כוחות": None,
        "1.3 מיקום המפקד המאפשר שליטה בכוח (לא להישאב לרובאות)": None
    },
    "עבודת קשר": {
        "2.1 נדב\"ר בסיסי - עלייה לפי פורמט": None,
        "2.2 אסרטיביות ופיקוד בדגש על שליטה בכוח ומניעת קשקשת ברשת": None,
        "2.3 דיווחים והכרזות בדגש על סיווג ואיפיון האירוע": None,
        "2.4 וידוא קבלה בעיקר בציון ידיעות חשובות": None
    },
    "מבצעיות | עקרונות לחימה": {
        "3.1 שימוש בשפה משותפת": None,
        "3.2 פכת\"ט | רואה, מעריך, ממליץ - דיווחים קצרים ומדוייקים": None,
        "3.3 מתן מענה לאירועים, קבלת החלטות נכונות": None,
        "3.4 שימוש במעטפת - כוחות חבירים, תצפיות וכו'": None,
        "3.5 הזדהות, חבירה וסגירת מעגלים - בדגש על מניעת דו\"צים": None
    }
}

# Define states
COLLECT_GRADES, COLLECT_YOUTUBE_LINK = range(4, 6)  # Adjust state numbers as needed

async def collect_grades_telegram(update, context):
    """
    Collects grades via Telegram conversation.
    """
    user_data = context.user_data

    if 'grades_data' not in user_data:
        # Initialize grades data
        user_data['grades_data'] = {}
        user_data['parts_iter'] = iter(parts.items())
        user_data['current_part'] = None
        user_data['items_iter'] = None
        user_data['current_item'] = None
        user_data['collecting_comment'] = False

    if user_data.get('collecting_comment'):
        # Collect comment
        comment = update.message.text
        part_name = user_data['current_part']
        user_data['grades_data'][part_name]['comment'] = comment

        # Calculate average for the part
        items = user_data['grades_data'][part_name]['items']
        part_average = round(sum(items.values()) / len(items), 2)
        user_data['grades_data'][part_name]['average'] = part_average

        # Reset current part and move to next
        user_data['current_part'] = None
        user_data['collecting_comment'] = False

    if user_data['current_part'] is None:
        # Move to next part
        try:
            part_name, items = next(user_data['parts_iter'])
            user_data['current_part'] = part_name
            user_data['grades_data'][part_name] = {'items': {}, 'comment': ''}
            user_data['items_iter'] = iter(items.keys())
            await update.message.reply_text(f"אנא הזינו ציונים עבור החלק: {part_name}")
        except StopIteration:
            # No more parts, proceed to collect YouTube link
            # Calculate final grade
            grades_data = user_data['grades_data']
            total_parts = len(grades_data)
            total_parts_score = sum([part['average'] for part in grades_data.values()])
            final_grade = round(total_parts_score / total_parts, 2)
            grades_data['final_grade'] = final_grade
            user_data['grades_data'] = grades_data

            # Move to collect YouTube link
            await update.message.reply_text('אנא הכנס את קישור סרטון התרגיל:(או הקלד "לא" אם אין)')
            return COLLECT_YOUTUBE_LINK

    # Collect grades for items
    if user_data['items_iter'] is not None:
        try:
            if user_data['current_item'] is None:
                # Ask for the next item's grade
                item_name = next(user_data['items_iter'])
                user_data['current_item'] = item_name
                await update.message.reply_text(f"ציון עבור {item_name} (1-10):")
                return COLLECT_GRADES
            else:
                # Collect the grade
                grade_text = update.message.text
                try:
                    grade = float(grade_text)
                    if not 1 <= grade <= 10:
                        raise ValueError
                except ValueError:
                    await update.message.reply_text("אנא הזינו ציון תקין בין 1 ל-10.")
                    return COLLECT_GRADES

                # Save the grade
                part_name = user_data['current_part']
                item_name = user_data['current_item']
                user_data['grades_data'][part_name]['items'][item_name] = grade
                user_data['current_item'] = None  # Reset current item

                # Ask for the next item's grade
                return await collect_grades_telegram(update, context)

        except StopIteration:
            # No more items in this part, ask for comment
            user_data['items_iter'] = None  # Reset items iterator
            user_data['collecting_comment'] = True
            await update.message.reply_text("אנא הזינו הערות עבור החלק (או השאירו ריק):")
            return COLLECT_GRADES

    return COLLECT_GRADES  # Continue collecting grades
