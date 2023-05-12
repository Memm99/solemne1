
! function($) {
    'use strict'

    var Class = function(el, cb) {
        this.$el = $(el);
        this.cb = cb;
        this.watch();
        return this;
    };

    Class.prototype = {

        /**
         *
         *
         * @returns {boolean}
         * Launch a callback indicating when the element is in and when is out.
         */
        watch: function() {
            var _self = this;
            var _isIn = false;

            $(window).on('resize scroll', function() {

                if (_self.isIn() && _isIn === false) {
                    _self.cb.call(_self.$el, 'entered');
                    _isIn = true;
                }

                if (_isIn === true && !_self.isIn()) {
                    _self.cb.call(_self.$el, 'leaved');
                    _isIn = false;
                }

            })
        }


    };

   
    $.fn.isInViewport = function(cb) {
        return this.each(function() {
            var $element = $(this);
            var data = $element.data('isInViewport');
            if (!data) {
                $element.data('isInViewport', (new Class(this, cb)));
            }
        })
    }

}(window.jQuery);