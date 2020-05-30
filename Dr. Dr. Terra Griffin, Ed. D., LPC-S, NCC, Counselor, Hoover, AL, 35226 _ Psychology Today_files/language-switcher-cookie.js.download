(function() {
  const preferredLanguageDataAttributeName = "data-preferred-language";

  /**
   * Sets a browser cookie to remember the preferred language
   * @param event
   */
  function setPreferredLanguageEventHandler(event) {
    document.cookie =
      "preferred_language=" +
      event.target.getAttribute(preferredLanguageDataAttributeName) +
      ";domain=" +
      getCookieDomain() +
      ";expires=Fri, 31 Dec 9999 23:59:59 GMT" +
      ";path=/";
  }

  /**
   * Returns the outer-most domain
   * @returns {string}
   */
  function getCookieDomain() {
    const locationParts = window.location.host.split(".");

    return locationParts
      .splice(Math.max(locationParts.length - 2), 2)
      .join(".");
  }

  // Setup click handlers on all language selector links
  Array.prototype.forEach.call(
    document.querySelectorAll("[" + preferredLanguageDataAttributeName + "]"),
    function(languageLink) {
      languageLink.addEventListener("click", setPreferredLanguageEventHandler);
    }
  );
})();
