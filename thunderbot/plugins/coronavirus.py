from covid import Covid
from thunderbot import CMD_HELP


@thunderbot.on(admin_cmd(pattern="coronavirus (.*)"))
@thunderbot.on(sudo_cmd(pattern="coronavirus (.*)", allow_sudo=True))
async def _(event):
    await event.edit("Collecting Data With The Help Of ThunderUserbot⚡️")
    country = event.pattern_match.group(1)
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
        output_text = (
            f"**Confirmed**   : {format_integer(country_data['confirmed'])}\n"
            + f"**Active**      : {format_integer(country_data['active'])}\n"
            + f"**Deaths**      : {format_integer(country_data['deaths'])}\n"
            + f"**Recovered**   : {format_integer(country_data['recovered'])}\n\n"
            + f"**New Cases**   : {format_integer(country_data['new_cases'])}\n"
            + f"**New Deaths**  : {format_integer(country_data['new_deaths'])}\n"
            + f"**Critical**    : {format_integer(country_data['critical'])}\n"
            + f"**Total Tests** : {format_integer(country_data['total_tests'])}\n\n"
            + f"**Data Collected By** ⚡️[ThunderUserbot](https://t.me/thunderuserbot)"
        )
        await event.edit(f"🦠Coronavirus Info In {country}:\n\n{output_text}")
    except ValueError:
        await event.edit(
            f"No Results Found For: {country}!\n😵Please Try Again After Sometime."
        )


def format_integer(number, thousand_separator="."):
    def reverse(string):
        string = "".join(reversed(string))
        return string

    s = reverse(str(number))
    count = 0
    result = ""
    for char in s:
        count = count + 1
        if count % 3 == 0:
            if len(s) == count:
                result = char + result
            else:
                result = thousand_separator + char + result
        else:
            result = char + result
    return result


CMD_HELP.update(
    {
        "coronavirus": ".coronavirus <country>"
        "\nUsage: Get information about Coronavirus in requested country.\n"
    }
)
