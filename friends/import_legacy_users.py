from dateutil import parser
from . import models
import csv
import pytz


def import_legacy_users():

    # questions and answers

    q_qualities = models.SurveyQuestion.objects.get(
        text='What are the 3 most important qualities to you in meeting & friending someone?',
        max_answers=3,
    )
    a_qualities_0 = models.SurveyAnswer.objects.get(
        question=q_qualities,
        order_index=0,
        text='Background or subculture',
    )
    a_qualities_1 = models.SurveyAnswer.objects.get(
        question=q_qualities,
        order_index=1,
        text='Chemistry / “gut feeling”',
    )
    a_qualities_2 = models.SurveyAnswer.objects.get(
        question=q_qualities,
        order_index=2,
        text='Curiosity (esp. intellectual)',
    )
    a_qualities_3 = models.SurveyAnswer.objects.get(
        question=q_qualities,
        order_index=3,
        text='Interests - music, movies, food, hobbies, etc.',
    )
    a_qualities_4 = models.SurveyAnswer.objects.get(
        question=q_qualities,
        order_index=4,
        text='Looks',
    )
    a_qualities_5 = models.SurveyAnswer.objects.get(
        question=q_qualities,
        order_index=5,
        text='Personality/Demeanor',
    )
    a_qualities_6 = models.SurveyAnswer.objects.get(
        question=q_qualities,
        order_index=6,
        text='Shared sense of humor',
    )
    a_qualities_7 = models.SurveyAnswer.objects.get(
        question=q_qualities,
        order_index=7,
        text='Shared values',
    )
    q_meeting = models.FreeTextQuestion.objects.get(
        text='What are your favorite ways or services for meeting people?',
    )
    q_inperson = models.SurveyQuestion.objects.get(
        text='How important is it to you to be able to meet up in person with someone you\'re matched with?',
    )
    a_inperson_0 = models.SurveyAnswer.objects.get(
        question=q_inperson,
        order_index=0,
        text='1',
    )
    a_inperson_1 = models.SurveyAnswer.objects.get(
        question=q_inperson,
        order_index=1,
        text='2',
    )
    a_inperson_2 = models.SurveyAnswer.objects.get(
        question=q_inperson,
        order_index=2,
        text='3',
    )
    a_inperson_3 = models.SurveyAnswer.objects.get(
        question=q_inperson,
        order_index=3,
        text='4',
    )
    a_inperson_4 = models.SurveyAnswer.objects.get(
        question=q_inperson,
        order_index=4,
        text='5',
    )
    q_museum = models.SurveyQuestion.objects.get(
        text='You must visit a museum. You would you rather go to an \\_\\_\\_\\_\\_ museum',
    )
    a_museum_0 = models.SurveyAnswer.objects.get(
        question=q_museum,
        order_index=0,
        text='art',
    )
    a_museum_1 = models.SurveyAnswer.objects.get(
        question=q_museum,
        order_index=1,
        text='history',
    )
    q_travelalone = models.SurveyQuestion.objects.get(
        text='Have you ever traveled around another country alone?',
    )
    a_travelalone_0 = models.SurveyAnswer.objects.get(
        question=q_travelalone,
        order_index=0,
        text='yes',
    )
    a_travelalone_1 = models.SurveyAnswer.objects.get(
        question=q_travelalone,
        order_index=1,
        text='no',
    )
    q_political = models.SurveyQuestion.objects.get(
        text='Can someone both be a kind person and also hold the exact opposite of your political views?',
    )
    a_political_0 = models.SurveyAnswer.objects.get(
        question=q_political,
        order_index=0,
        text='yes',
    )
    a_political_1 = models.SurveyAnswer.objects.get(
        question=q_political,
        order_index=1,
        text='no',
    )
    q_niche = models.SurveyQuestion.objects.get(
        text='Do you belong to at least one online community focused around niche interests?',
    )
    a_niche_0 = models.SurveyAnswer.objects.get(
        question=q_niche,
        order_index=0,
        text='yes',
    )
    a_niche_1 = models.SurveyAnswer.objects.get(
        question=q_niche,
        order_index=1,
        text='no',
    )
    q_suicide = models.SurveyQuestion.objects.get(
        text='If you have to choose one, you believe suicide should be:',
    )
    a_suicide_0 = models.SurveyAnswer.objects.get(
        question=q_suicide,
        order_index=0,
        text='legal',
    )
    a_suicide_1 = models.SurveyAnswer.objects.get(
        question=q_suicide,
        order_index=1,
        text='illegal',
    )
    q_rules = models.SurveyQuestion.objects.get(
        text='I feel \\_\\_\\_\\_\\_\\_\\_ around people who break rules.',
    )
    a_rules_0 = models.SurveyAnswer.objects.get(
        question=q_rules,
        order_index=0,
        text='comfortable',
    )
    a_rules_1 = models.SurveyAnswer.objects.get(
        question=q_rules,
        order_index=1,
        text='uncomfortable',
    )
    q_horror = models.SurveyQuestion.objects.get(
        text='Do you like horror movies?',
    )
    a_horror_0 = models.SurveyAnswer.objects.get(
        question=q_horror,
        order_index=0,
        text='yes',
    )
    a_horror_1 = models.SurveyAnswer.objects.get(
        question=q_horror,
        order_index=1,
        text='no',
    )
    q_jail = models.SurveyQuestion.objects.get(
        text='I daydream about how I would escape from jail.',
    )
    a_jail_0 = models.SurveyAnswer.objects.get(
        question=q_jail,
        order_index=0,
        text='yes',
    )
    a_jail_1 = models.SurveyAnswer.objects.get(
        question=q_jail,
        order_index=1,
        text='no',
    )
    q_pranks = models.SurveyQuestion.objects.get(
        text='I like pranks.',
    )
    a_pranks_0 = models.SurveyAnswer.objects.get(
        question=q_pranks,
        order_index=0,
        text='yes',
    )
    a_pranks_1 = models.SurveyAnswer.objects.get(
        question=q_pranks,
        order_index=1,
        text='no',
    )
    q_enlighten = models.SurveyQuestion.objects.get(
        text='It is possible to obtain enlightenment through meditation.',
    )
    a_enlighten_0 = models.SurveyAnswer.objects.get(
        question=q_enlighten,
        order_index=0,
        text='yes',
    )
    a_enlighten_1 = models.SurveyAnswer.objects.get(
        question=q_enlighten,
        order_index=1,
        text='no',
    )
    q_boat = models.SurveyQuestion.objects.get(
        text='Wouldn\'t it be fun to chuck it all and go live on a sailboat?',
    )
    a_boat_0 = models.SurveyAnswer.objects.get(
        question=q_boat,
        order_index=0,
        text='yes',
    )
    a_boat_1 = models.SurveyAnswer.objects.get(
        question=q_boat,
        order_index=1,
        text='no',
    )
    q_jokes = models.SurveyQuestion.objects.get(
        text='I make jokes that offend some people.',
    )
    a_jokes_0 = models.SurveyAnswer.objects.get(
        question=q_jokes,
        order_index=0,
        text='yes',
    )
    a_jokes_1 = models.SurveyAnswer.objects.get(
        question=q_jokes,
        order_index=1,
        text='no',
    )
    q_similar = models.SurveyQuestion.objects.get(
        text='My friends are mostly \\_\\_\\_\\_\\_\\_\\_ me.',
    )
    a_similar_0 = models.SurveyAnswer.objects.get(
        question=q_similar,
        order_index=0,
        text='similar to',
    )
    a_similar_1 = models.SurveyAnswer.objects.get(
        question=q_similar,
        order_index=1,
        text='different from',
    )
    q_evolution = models.SurveyQuestion.objects.get(
        text='I believe in evolution.',
    )
    a_evolution_0 = models.SurveyAnswer.objects.get(
        question=q_evolution,
        order_index=0,
        text='yes',
    )
    a_evolution_1 = models.SurveyAnswer.objects.get(
        question=q_evolution,
        order_index=1,
        text='no',
    )
    q_parties = models.SurveyQuestion.objects.get(
        text='I enjoy going to parties even if I don\'t know anyone.',
    )
    a_parties_0 = models.SurveyAnswer.objects.get(
        question=q_parties,
        order_index=0,
        text='yes',
    )
    a_parties_1 = models.SurveyAnswer.objects.get(
        question=q_parties,
        order_index=1,
        text='no',
    )
    q_promise = models.SurveyQuestion.objects.get(
        text='I keep my word and expect others to.',
    )
    a_promise_0 = models.SurveyAnswer.objects.get(
        question=q_promise,
        order_index=0,
        text='yes',
    )
    a_promise_1 = models.SurveyAnswer.objects.get(
        question=q_promise,
        order_index=1,
        text='no',
    )
    q_secrets = models.SurveyQuestion.objects.get(
        text='I keep secrets well.',
    )
    a_secrets_0 = models.SurveyAnswer.objects.get(
        question=q_secrets,
        order_index=0,
        text='yes',
    )
    a_secrets_1 = models.SurveyAnswer.objects.get(
        question=q_secrets,
        order_index=1,
        text='no',
    )
    q_conflict = models.SurveyQuestion.objects.get(
        text='I tend to avoid conflict.',
    )
    a_conflict_0 = models.SurveyAnswer.objects.get(
        question=q_conflict,
        order_index=0,
        text='yes',
    )
    a_conflict_1 = models.SurveyAnswer.objects.get(
        question=q_conflict,
        order_index=1,
        text='no',
    )
    q_horoscopes = models.SurveyQuestion.objects.get(
        text='I think horoscopes are fun.',
    )
    a_horoscopes_0 = models.SurveyAnswer.objects.get(
        question=q_horoscopes,
        order_index=0,
        text='yes',
    )
    a_horoscopes_1 = models.SurveyAnswer.objects.get(
        question=q_horoscopes,
        order_index=1,
        text='no',
    )
    q_fiction = models.SurveyQuestion.objects.get(
        text='Fictional stories (books, film, TV series, etc) are one of my most common conversational topics.',
    )
    a_fiction_0 = models.SurveyAnswer.objects.get(
        question=q_fiction,
        order_index=0,
        text='yes',
    )
    a_fiction_1 = models.SurveyAnswer.objects.get(
        question=q_fiction,
        order_index=1,
        text='no',
    )
    q_trans = models.SurveyQuestion.objects.get(
        text='I would be open to dating a transsexual person.',
    )
    a_trans_0 = models.SurveyAnswer.objects.get(
        question=q_trans,
        order_index=0,
        text='yes',
    )
    a_trans_1 = models.SurveyAnswer.objects.get(
        question=q_trans,
        order_index=1,
        text='no',
    )
    q_controversial = models.SurveyQuestion.objects.get(
        text='Do you hold any controversial views (on society, politics, culture, etc.) that you would feel afraid to express on social media or to your wider friend group?',
    )
    a_controversial_0 = models.SurveyAnswer.objects.get(
        question=q_controversial,
        order_index=0,
        text='yes',
    )
    a_controversial_1 = models.SurveyAnswer.objects.get(
        question=q_controversial,
        order_index=1,
        text='no',
    )
    q_smartdrugs = models.SurveyQuestion.objects.get(
        text='I would take drugs to make myself smarter if they existed.',
    )
    a_smartdrugs_0 = models.SurveyAnswer.objects.get(
        question=q_smartdrugs,
        order_index=0,
        text='yes',
    )
    a_smartdrugs_1 = models.SurveyAnswer.objects.get(
        question=q_smartdrugs,
        order_index=1,
        text='no',
    )
    q_commitment = models.SurveyQuestion.objects.get(
        text='My choices mostly reflect a commitment to \\_\\_\\_\\_\\_\\_\\_.',
    )
    a_commitment_0 = models.SurveyAnswer.objects.get(
        question=q_commitment,
        order_index=0,
        text='myself',
    )
    a_commitment_1 = models.SurveyAnswer.objects.get(
        question=q_commitment,
        order_index=1,
        text='my loved ones',
    )
    q_openup = models.SurveyQuestion.objects.get(
        text='It takes me longer than average to open up / become comfortable around strangers.',
    )
    a_openup_0 = models.SurveyAnswer.objects.get(
        question=q_openup,
        order_index=0,
        text='yes',
    )
    a_openup_1 = models.SurveyAnswer.objects.get(
        question=q_openup,
        order_index=1,
        text='no',
    )
    q_worry = models.SurveyQuestion.objects.get(
        text='I worry my friends or partners will leave me.',
    )
    a_worry_0 = models.SurveyAnswer.objects.get(
        question=q_worry,
        order_index=0,
        text='yes',
    )
    a_worry_1 = models.SurveyAnswer.objects.get(
        question=q_worry,
        order_index=1,
        text='no',
    )

    with open('legacy_users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        count = 1
        for row in reader:
            print('Importing row {}'.format(count))
            count += 1

            # User data

            good_user = row['Good User?'] == 'TRUE'
            name = row['What would you like to be called?'][:models.FIRST_NAME_MAX_LENGTH]
            entry_round = int(row['Entry Round'])
            email = row['Email'].lower()[:models.EMAIL_MAX_LENGTH]
            telegram = row['Telegram account'][:models.LEGACY_TELEGRAM_MAX_LENGTH]
            raw_gender = row['What\'s your current gender identity?']
            if raw_gender == 'Male':
                gender = models.GENDER_ID_MALE
            elif raw_gender == 'Female':
                gender = models.GENDER_ID_FEMALE
            else:
                gender = models.GENDER_ID_OTHER
            age = int(row['What\'s your age?'])
            location = row['What\'s your location?'][:models.CITY_MAX_LENGTH]
            expect_match_well = row['How well do you think we could match you based on these questions?'] == 'Well'
            missing_from_questions = row['What, if anything, do you think is missing from our questions?']
            submitted_at = pytz.UTC.localize(parser.parse(row['Submitted At']))
            token = row['Token'][:models.LEGACY_TOKEN_MAX_LENGTH]
            user = models.LunaUser.objects.create_user(
                username=email,
                email=email,
                first_name=name,
                city=location,
                date_joined=submitted_at,
            )
            models.LegacyDataSet.objects.create(
                user=user,
                good_user=good_user,
                name=name,
                entry_round=entry_round,
                telegram=telegram,
                gender=gender,
                age=age,
                location=location,
                expect_match_well=expect_match_well,
                missing_from_questions=missing_from_questions,
                submitted_at=submitted_at,
                token=token,
            )

            # Question data

            # What are the 3 most important qualities to you in meeting & friending someone?

            r_qualities = row[q_qualities.text]
            for a_qualities_x in [
                a_qualities_0,
                a_qualities_1,
                a_qualities_2,
                a_qualities_3,
                a_qualities_4,
                a_qualities_5,
                a_qualities_6,
                a_qualities_7,
            ]:
                if a_qualities_x.text in r_qualities:
                    models.SurveyResponse.objects.create(
                        user=user,
                        answer=a_qualities_x,
                        timestamp=submitted_at,
                    )

            # What are your favorite ways or services for meeting people?

            r_meeting = row[q_meeting.text]
            models.FreeTextResponse.objects.create(
                user=user,
                question=q_meeting,
                text=r_meeting,
                timestamp=submitted_at,
            )

            # How important is it to you to be able to meet up in person with someone you're matched with?

            r_inperson = row[q_inperson.text]
            for a_inperson_x in [
                a_inperson_0,
                a_inperson_1,
                a_inperson_2,
                a_inperson_3,
                a_inperson_4,
            ]:
                if a_inperson_x.text == r_inperson:
                    models.SurveyResponse.objects.create(
                        user=user,
                        answer=a_inperson_x,
                        timestamp=submitted_at,
                    )

            # You must visit a museum. You would you rather go to an \_\_\_\_\_ museum

            r_museum = row[q_museum.text]
            for a_museum_x in [
                a_museum_0,
                a_museum_1,
            ]:
                if a_museum_x.text == r_museum:
                    models.SurveyResponse.objects.create(
                        user=user,
                        answer=a_museum_x,
                        timestamp=submitted_at,
                    )

            # Have you ever traveled around another country alone?

            r_travelalone = row[q_travelalone.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_travelalone_0 if r_travelalone else a_travelalone_1,
                timestamp=submitted_at,
            )

            # Can someone both be a kind person and also hold the exact opposite of your political views?

            r_political = row[q_political.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_political_0 if r_political else a_political_1,
                timestamp=submitted_at,
            )

            # Do you belong to at least one online community focused around niche interests?

            # text differs between csv and migration, hence not looking up by question text field
            r_niche = row['I belong to online communities focused around niche interests.'] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_niche_0 if r_niche else a_niche_1,
                timestamp=submitted_at,
            )

            # If you have to choose one, you believe suicide should be:

            # text differs between csv and migration, hence not looking up by question text field
            r_suicide = row['Do you prefer to live in a world where suicide is legal or illegal?'] == 'legal'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_suicide_0 if r_suicide else a_suicide_1,
                timestamp=submitted_at,
            )

            # I feel \_\_\_\_\_\_\_ around people who break rules.

            r_rules = row[q_rules.text] == 'comfortable'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_rules_0 if r_rules else a_rules_1,
                timestamp=submitted_at,
            )

            # Do you like horror movies?

            r_horror = row[q_horror.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_horror_0 if r_horror else a_horror_1,
                timestamp=submitted_at,
            )

            # I daydream about how I would escape from jail.

            r_jail = row[q_jail.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_jail_0 if r_jail else a_jail_1,
                timestamp=submitted_at,
            )

            # I like pranks.

            r_pranks = row[q_pranks.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_pranks_0 if r_pranks else a_pranks_1,
                timestamp=submitted_at,
            )

            # It is possible to obtain enlightenment through meditation.

            r_enlighten = row[q_enlighten.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_enlighten_0 if r_enlighten else a_enlighten_1,
                timestamp=submitted_at,
            )

            # Wouldn't it be fun to chuck it all and go live on a sailboat?

            r_boat = row[q_boat.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_boat_0 if r_boat else a_boat_1,
                timestamp=submitted_at,
            )

            # I make jokes that offend some people.

            r_jokes = row[q_jokes.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_jokes_0 if r_jokes else a_jokes_1,
                timestamp=submitted_at,
            )

            # My friends are mostly \_\_\_\_\_\_\_ me.

            r_similar = row[q_similar.text] == 'similar to'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_similar_0 if r_similar else a_similar_1,
                timestamp=submitted_at,
            )

            # I believe in evolution.

            r_evolution = row[q_evolution.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_evolution_0 if r_evolution else a_evolution_1,
                timestamp=submitted_at,
            )

            # I enjoy going to parties even if I don't know anyone.

            r_parties = row[q_parties.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_parties_0 if r_parties else a_parties_1,
                timestamp=submitted_at,
            )

            # I keep my word and expect others to.

            r_promise = row[q_promise.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_promise_0 if r_promise else a_promise_1,
                timestamp=submitted_at,
            )

            # I keep secrets well.

            r_secrets = row[q_secrets.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_secrets_0 if r_secrets else a_secrets_1,
                timestamp=submitted_at,
            )

            # I tend to avoid conflict.

            r_conflict = row[q_conflict.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_conflict_0 if r_conflict else a_conflict_1,
                timestamp=submitted_at,
            )

            # I think horoscopes are fun.

            r_horoscopes = row[q_horoscopes.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_horoscopes_0 if r_horoscopes else a_horoscopes_1,
                timestamp=submitted_at,
            )

            # Fictional stories (books, film, TV series, etc) are one of my most common conversational topics.

            r_fiction = row[q_fiction.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_fiction_0 if r_fiction else a_fiction_1,
                timestamp=submitted_at,
            )

            # I would be open to dating a transsexual person.

            r_trans = row[q_trans.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_trans_0 if r_trans else a_trans_1,
                timestamp=submitted_at,
            )

            # Do you hold any controversial views (on society, politics, culture, etc.) that you would feel afraid to express on social media or to your wider friend group?

            r_controversial = row[q_controversial.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_controversial_0 if r_controversial else a_controversial_1,
                timestamp=submitted_at,
            )

            # I would take drugs to make myself smarter if they existed.

            r_smartdrugs = row[q_smartdrugs.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_smartdrugs_0 if r_smartdrugs else a_smartdrugs_1,
                timestamp=submitted_at,
            )

            # My choices mostly reflect a commitment to \_\_\_\_\_\_\_.

            r_commitment = row[q_commitment.text] == 'myself'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_commitment_0 if r_commitment else a_commitment_1,
                timestamp=submitted_at,
            )

            # It takes me longer than average to open up / become comfortable around strangers.

            r_openup = row[q_openup.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_openup_0 if r_openup else a_openup_1,
                timestamp=submitted_at,
            )

            # I worry my friends or partners will leave me.

            r_worry = row[q_worry.text] == 'TRUE'
            models.SurveyResponse.objects.create(
                user=user,
                answer=a_worry_0 if r_worry else a_worry_1,
                timestamp=submitted_at,
            )
