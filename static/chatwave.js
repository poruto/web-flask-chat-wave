
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

function delay (miliseconds) 
    {
        return new Promise((resolve) => {
            window.setTimeout(() => {
                resolve();
            }, miliseconds);
        });
    }

var setInnerHTML = function(elm, html) {
        elm.innerHTML = html;
        Array.from(elm.querySelectorAll("script")).forEach( oldScript => {
            const newScript = document.createElement("script");
            Array.from(oldScript.attributes)
            .forEach( attr => newScript.setAttribute(attr.name, attr.value) );
            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
        }