var keys = {
    ESC: 27,
    TAB: 9,
    RETURN: 13,
    LEFT: 37,
    UP: 38,
    RIGHT: 39,
    DOWN: 40
};

$(document).ready(function () {

    $('#autosuggestSearchInput, input[data-trigger=search-autosuggest]').val('');
    var attributeSearchField = $('[data-trigger=search-autosuggest][data-attribute-id]');

    var autosuggestContainer = $('#autosuggestContainer');
    var placeholder = autosuggestContainer.data('placeholder');
    var requestUrl = autosuggestContainer.data('endpoint');
    var resultsUrl = autosuggestContainer.data('results-endpoint');
    var findCopy = autosuggestContainer.data('find-copy');

    if (attributeSearchField.length) {
        requestUrl = requestUrl + '?attributes[]=' + attributeSearchField.data('attribute-id');
        placeholder = attributeSearchField.attr('placeholder');
    }

	var options = {
        requestUrl: requestUrl,
        resultsUrl: resultsUrl,
        placeholder: placeholder,
        formatResult: function (index, suggestion) {
            var label = 'Search_LocationSuggestion';
            var separator = suggestion.caption ? ",&nbsp;" : "&nbsp;";
            if (suggestion.group == 'names') {
                label = 'Search_NameSuggestion';
                separator = suggestion.caption ? "&nbsp;-&nbsp;" : separator;
            }

            return "<a class='suggestion " + suggestion.type + "' " +
                "title=\"" + suggestion.value + "\" href=\"" + suggestion.url + "\" data-index='" + index + "' " +
                "data-event-label='" + label + "' data-event-value='" + (index + 1) + "'>" +
                "<span class='title h5'>" + suggestion.title + separator + "</span>" +
                "<span class='caption h5'>" + suggestion.caption + "</span>" +
                "</a>";
        },
        formatNoResult: function (sectionName) {
            return "";
        },
        formatEndOfResults: function (searchString, sectionName, index, url) {
            var classes = ['suggestion'];
            var label = 'Search_MoreNamesSuggestion';
            var title = 'More&nbsp;...';
            var caption = '';

            if (sectionName == 'locations') {
                label = 'Search_FindByNameSuggestion';
                title = findCopy;
                caption = '"' + searchString + '"';
                classes.push('separator');
            }

            return "<a href='" + url + "' class='" + classes.join(' ') + "' title='" + title + "' " +
                "data-index='" + index + "' data-event-label='" + label + "'>" +
                "<span class='title h5'>" + title + "</span>" +
                (caption ? "&nbsp;<span class='title h5'><strong>" + caption + "</strong></span>" : "") +
                "</a>"
        }
    };

    autosuggestContainer.autosuggest(options);

    $('#searchSuggestionsWrapper').on('touchmove', function (event) {
        $('#autosuggestContainer').trigger('blurInput');
    });

    $(window)
        .on('resize', function () {
            $('#autosuggestContainer').trigger('resizeSuggestions');
        });

});

(function ($) {

    $.fn.autosuggest = $.fn.sussexAutosuggest = function (options) {
        return new Autosuggest(this, options);
    };

    function Autosuggest(element, options) {

        var that = this;
        var defaults = {
            requestUrl: null,
            resultsUrl: null,
            maxResults: 20,
            minHeight: 80,
            maxHeight: 965,
            highlightTextMatch: true,
            formatResult: function (index, suggestion) {
                that.formatResult(index, suggestion);
            },
            formatNoResult: that.formatNoResult,
            formatEndOfResults: that.formatEndOfResults
        };

        // Store a reference to the auto suggest object on the element
        element.data('autosuggest', this);

        that.container = $(element);
        that.inputField = $('#autosuggestSearchInput');
        that.hiddenInputField = $('#autosuggestHiddenInput');
        that.messageContainer = that.container.find('.autosuggest-message');
        that.options = $.extend(defaults, options);

        this.container.off();
        this.container.find('.autosuggest-section').off();
        this.inputField.off();

        this.container.on('click', '.suggestion', function () {
            if ($(this).hasClass('wait')) {
                return false;
            } else {
                that.setActiveSuggestion($(this).data('index'), true);
            }
        });

        this.container.on('mouseenter', '.suggestion', function () {
            that.highlightSuggestion($(this).data('index'), true);
        });
        this.container.on('mouseleave', '.suggestion', function () {
            that.highlightSuggestion(that.activeSuggestionIndex, false);
        });

        this.container.on('keydown', function (event) {
            that.onKeyDown(event);
        });

        this.container.on('click', '.btn-search', function () {
            event.preventDefault();
            if (that.inputField.val() == "") {
                that.geolocationSearch();
            } else {
                that.initiateSearch();
            }
        });

        this.container.on('clearSuggestions', function () {
            that.clearSuggestions();
        });

        this.container.on('resizeSuggestions', function () {
            that.resizeSuggestions();
        });

        this.container.on('blurInput', function () {
            that.inputField.blur();
        });

        this.inputField.on('input', function (event) {
            that.onInput(event);
            that.forceReflow(that.inputField);
        });

        this.inputField.on('focus', function (event) {
            $('body').scrollTop(0);
            that.container.find('.autosuggest-sections').scrollTop(0);
            that.forceScrollFix();
        });

    }

    Autosuggest.prototype = {

        activeSuggestionIndex: -1,
        lastQuery: '',

        fetchSuggestions: function (requestData) {

            var that = this;

            var suggestionContainers = that.container.find('.autosuggest-section');

            var sections = [];
            if (!requestData.sections) {
                suggestionContainers.each(function (index, container) {
                    sections.push($(container).data('section'));
                });
                requestData.sections = sections;
            }

            var sameQuery = requestData.query && requestData.query == that.lastQuery;

            if (!requestData.query) {
                that.abortRequest();
                that.clearSuggestions();
                $('.autosuggest-container').removeClass('active');
                return false;
            } else if (sameQuery) {
                return false;
            }

            this.abortRequest();
            that.lastQuery = requestData.query;

            this.currentRequest = $.getJSON(this.options.requestUrl, requestData, function (response) {
                var i = 0;
                $.each(suggestionContainers, function (index, suggestionContainer) {
                    var scrollTop = $(suggestionContainer).scrollTop();
                    var section = $(suggestionContainer).data('section');
                    if (response.groups[section].length > 0) {
                        var html = '';
                        var count = response.groups[section].length;
                        var searchString = that.inputField.val();

                        $('.autosuggest-container').addClass('active');
                        $(suggestionContainer).data('suggestion-count', count);

                        $.each(response.groups[section], function (index, suggestion) {

                            if (that.options.highlightTextMatch) {
                                suggestion.title = that.highlightText(searchString, suggestion.title);
                            }

                            html += that.options.formatResult(i, suggestion);
                            i++;
                        });

                        $(suggestionContainer).html(html).addClass('has-suggestions');

                        if (response.nameSearchUrl) {
                            var endIndex = response.groups[section].length;
                            $(suggestionContainer).append(
                                that.options.formatEndOfResults(searchString, section, endIndex, response.nameSearchUrl)
                            );
                        }
                    } else {
                        $(suggestionContainer)
                            .html(that.options.formatNoResult(section))
                            .removeClass('has-suggestions');
                    }

                    if (that.suggestions().length == 0) {
                        $('.autosuggest-container').removeClass('active');
                    }

                    that.setActiveSuggestion(0, false);
                    $(suggestionContainer).scrollTop(scrollTop);
                });

                that.resizeSuggestions();

            });
        },

        abortRequest: function () {
            if (this.currentRequest) {
                this.currentRequest.abort();
                this.currentRequest = null;
            }
        },

        onInput: function () {
            var that = this;
            var inputValue = that.inputField.val();
            that.hiddenInputField.val(inputValue);
            this.fetchSuggestions({query: inputValue, size: that.options.maxResults + 1});
        },

        onKeyDown: function (event) {
            var that = this;
            switch (event.which) {
                case keys.UP:
                    event.preventDefault();
                    event.stopPropagation();
                    that.setActiveSuggestion(that.activeSuggestionIndex - 1, true);
                    that.adjustScroll();
                    break;
                case keys.DOWN:
                    event.preventDefault();
                    event.stopPropagation();
                    that.setActiveSuggestion(that.activeSuggestionIndex + 1, true);
                    that.adjustScroll();
                    break;
                case keys.RETURN:
                    if (that.activeSuggestionIndex == 0) {
                        event.preventDefault();
                        event.stopPropagation();
                        if (that.inputField.val() == "") {
                            that.geolocationSearch();
                        } else {
                            that.initiateSearch();
                        }
                    } else if (that.activeSuggestion()) {
                        that.activeSuggestion()[0].click();
                    }
                    break;
                default:
                    break;
            }
        },

        clearSuggestions: function () {
            var that = this;
            that.lastQuery = '';
            $(that.inputField).val('');
            $(that.hiddenInputField).val('');
            that.sections().removeClass('has-suggestions').html('');
            that.container.removeClass('active');
            that.sections().hide().show(); // Hack to force a repaint for Edge
        },

        clearActiveSuggestion: function () {
            var that = this;
            that.activeSuggestionIndex = 0;
            that.highlightSuggestion(that.activeSuggestionIndex);
            that.inputField.val(that.hiddenInputField.val());
        },

        setActiveSuggestion: function (index, updateInput) {
            var that = this;

            if (index < 0) {
                that.clearActiveSuggestion();
            } else if (that.highlightSuggestion(index)) {
                that.activeSuggestionIndex = index;
                var activeSuggestion = that.suggestions(that.activeSuggestionIndex);
                activeSuggestion.addClass('active');
                if (updateInput && 0) {
                    that.inputField.val(activeSuggestion.attr('title'));
                }
            }
        },

        highlightText: function (searchString, suggestionText) {
            var decoder = document.createElement("textarea");
            decoder.innerHTML = suggestionText;
            suggestionText = decoder.value;
            var words = searchString.split(' ');

            if (words.length) {
                var regex = new RegExp('(\\s|^)(' + words.join('|') + ')', 'ig');

                return suggestionText.replace(regex, '$1<strong>$2</strong>');
            }

            return suggestionText;
        },

        highlightSuggestion: function (index, hover) {
            var that = this;
            var activeSuggestion = that.suggestions(index);

            if (index == -1) {
                that.suggestions().removeClass('active hover');
                return false;
            }

            if (!activeSuggestion.length) {
                return false;
            }

            if (hover) {
                that.suggestions().removeClass('hover');
                activeSuggestion.addClass('hover');
            } else {
                that.suggestions().removeClass('hover active');
                activeSuggestion.addClass('active');
            }

            return true;
        },

        selectSuggestion: function (index) {
            var that = this;
            var suggestion = that.suggestions(index);
            if (suggestion.length) {
                suggestion[0].click();
            } else {
                that.initiateSearch();
            }
        },

        geolocationSearch: function () {
            var that = this;
            navigator.geolocation.getCurrentPosition(function (position) {
                var ll = position.coords.latitude + "," + position.coords.longitude;
                var url = that.options.resultsUrl + '?ll=' + ll;
                var specialtyId = $('#spec').val();
                if (specialtyId) {
                    url += '&spec=' + specialtyId;
                }
                document.location.href = url;
            });
        },

        initiateSearch: function (sectionName) {
            var that = this;
            var query = $(that.hiddenInputField).val();
            var url = that.options.resultsUrl;

            dataLayer.push({
                'event': 'dataLayerEvent',
                'eventAction': 'click',
                'eventLabel': 'Search_Freeform'
            });

            document.location = url + (url.indexOf('?') === -1 ? '?' : '&') + 'search=' + query;
        },

        adjustScroll: function () {
            var that = this;
            var activeSuggestion = that.suggestions(that.activeSuggestionIndex);

            if (activeSuggestion.length) {
                var sectionsContainer = that.sectionsContainer();
                var suggestionOffset = activeSuggestion.offset().top + sectionsContainer.scrollTop();
                var containerOffset = that.container.offset().top + sectionsContainer.innerHeight();

                if (suggestionOffset >= containerOffset) {
                    sectionsContainer.scrollTop(suggestionOffset - containerOffset);
                } else {
                    sectionsContainer.scrollTop(0);
                }
            }
        },

        resizeSuggestions: function () {
            var that = this;
            var sections = that.container.find('.autosuggest-sections');
            var searchField = $('#searchField');

            var xsDevice = $('html').hasClass('device-xs');

            var paddingTop = 0;
            var buffer = (xsDevice) ? 0 : 15;

            that.inputField.attr('placeholder', that.container.data('placeholder'));

            var maxHeight = $(window).height() - buffer;

            maxHeight = maxHeight > that.options.maxHeight ? that.options.maxHeight : maxHeight;
            maxHeight = maxHeight < that.options.minHeight ? that.options.minHeight : maxHeight;
            sections.css('max-height', maxHeight);
            that.adjustScroll();
        },

        sectionsContainer: function () {
            var that = this;
            return that.container.find('.autosuggest-sections');
        },

        sections: function () {
            var that = this;
            return that.container.find('.autosuggest-section');
        },

        activeSection: function () {
            var that = this;
            return that.container.find('.autosuggest-section').first();
        },

        suggestions: function (index) {
            var that = this;
            var suggestions = that.sections().find('.suggestion');

            if (typeof index != 'undefined') {
                return suggestions.filter('[data-index=' + index + ']');
            }

            return suggestions;

        },

        activeSuggestion: function () {
            var that = this;
            var activeSuggestion = that.suggestions(that.activeSuggestionIndex);
            if (activeSuggestion.length) {
                return activeSuggestion;
            }

            return null;
        },

        formatResult: function (index, suggestion) {
            return "<div class='suggestion'>" + suggestion.value + "</div>";
        },

        formatNoResult: function (sectionName) {
            return "<div class='no-suggestion' data-section='" + sectionName + "'>No Results Found</div>";
        },

        formatEndOfResults: function (sectionName) {
            return "";
        },

        forceReflow: function (element) {
            var userAgent = userAgent || navigator.userAgent;
            var isInternetExplorer = userAgent.indexOf("MSIE ") > -1 || userAgent.indexOf("Trident/") > -1;
            var isEdge = userAgent.indexOf("Edge/") > -1;
            // Force a reflow to fix rendering issues common on iOS
            if (!isInternetExplorer && !isEdge) {
                $(element).hide();
                $(element).css('display');
                $(element).show();
            }
        },

        forceScrollFix: function() {
            // Check at arbitrary intervals to see if scroll changed, if so, reset it to deal with keyboards on iOS 13
            var lastScrollPosition = $(document).scrollTop();
            var timeouts = [50, 100, 150, 500];
            for (var i = 0; i < timeouts.length; i++) {
                setTimeout(function() {
                    if (lastScrollPosition !== $(document).scrollTop()) {
                        $(document).scrollTop(0);
                    }
                }, timeouts[i]);
            }
        }

    };


})(jQuery);
