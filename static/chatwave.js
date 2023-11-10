
function getCountryData()
{
    var obj = $("#country_selector").countrySelect("getSelectedCountryData");
    return obj;
}

function initCountrySelector()
{
    $("#country_selector").countrySelect({
        preferredCountries: ['cz', 'gb', 'ch', 'ca', 'do', 'us'],
        // localized country names e.g. { 'de': 'Deutschland' }
        localizedCountries: null,
        defaultCountry: 'us',
        defaultStyling:"inside",
        });
}

function setCountry(code)
{
    $("#country_selector").countrySelect("selectCountry", code);
}

function destroyCountrySelector()
{
    $("#country_selector").countrySelect("destroy");
}