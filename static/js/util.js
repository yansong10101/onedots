function scroll_carousel($container, $num) {
    var ul = $container.find('ul');
    var firstLi = $(ul.find('li').get(0));
    var secondLi = ul.find('li+li');
    var visibleEle = $container.find('.content_carousel');
    var prevArrow = $container.find('.arrow.prev');
    var nextArrow = $container.find('.arrow.next');

    var liLen = secondLi.width();
    var margLeftLi = parseInt(secondLi.css('margin-left'));
    firstLi.css('margin-left', margLeftLi / 2);
    var visibleLen = liLen * $num + margLeftLi * $num;
    var totalLen = ul.children().length * liLen + ul.children().length * margLeftLi;

    visibleEle.width(visibleLen);
    ul.width(totalLen);

    //console.log("li: " + liLen + ", margeLi: " + margLeftLi + ", visibleLen: " + visibleLen + ", totalLen: " + totalLen);

    var isNextClickable = true,
        isPrevClickable = true;

    function enableNext(isEnable) {
        if (isEnable) {
            nextArrow.css('visibility', 'visible');
            nextArrow.click(next);
        } else {
            nextArrow.css('visibility', 'hidden');
            nextArrow.off('click');
        }
    }

    function enablePrev(isEnable) {
        if (isEnable) {
            prevArrow.css('visibility', 'visible');
            prevArrow.click(prev);
        } else {
            prevArrow.css('visibility', 'hidden');
            prevArrow.off('click');
        }
    }

    function next() {
        if (!isNextClickable) {
            return;
        }
        isNextClickable = false;

        var margLeftUl = -parseInt(ul.css('margin-left'));
        if (margLeftUl + visibleLen >= totalLen) { // no more
            return;
        }

        ul.animate({
            'margin-left': '-=' + visibleLen
        }, 1000, function() {
            var margLeftUl = -parseInt(ul.css('margin-left'));
            //console.log("visibleLen: " + visibleLen + ", totalLen: " + totalLen + ", margLeftUl: " + margLeftUl);
            if (margLeftUl + visibleLen >= totalLen) { // no more
                enableNext(false);
            }
            isNextClickable = true;
            enablePrev(true);
        });
    }

    function prev() {
        if (!isPrevClickable) {
            return;
        }
        isPrevClickable = false;

        var margLeftUl = parseInt(ul.css('margin-left'));
        if (margLeftUl >= 0) {
            return;
        }

        enableNext(true);
        ul.animate({
            'margin-left': '+=' + visibleLen
        }, 1000, function() {
            var margLeftUl = parseInt(ul.css('margin-left'));
            //console.log("visibleLen: " + visibleLen + ", totalLen: " + totalLen + ", margLeftUl: " + margLeftUl);
            if (margLeftUl >= 0) { // no prev
                enablePrev(false);
            }
            isPrevClickable = true;
        });
    }

    function init() {
        var margLeftUl = -parseInt(ul.css('margin-left'));
        enablePrev(false);
        if (margLeftUl > 0) {
            console.error("Please set the margin-left as 0 when init");
        }
        enableNext(margLeftUl + visibleLen < totalLen)
    }

    function attachEvents() {
        nextArrow.click(next);
        prevArrow.click(prev);
    }

    init();
    attachEvents();
}


function changeQuantity($r, callback) {
    var unit_price = $r.find('.product_price').text().substr(1),
        $plus = $r.find('.plus'),
        $minus = $r.find('.minus'),
        $count = $r.find('.product-count'),
        $total = $r.find('.item_total_price'),
        $product_quantity = $r.find('.product-quantity');

    function init() {
        setCount($count.val() * 1 || 0);
    }

    function setCount(num) {
        $count.val(num);
        $total.text('$' + (num * unit_price));
        callback();
    }

    $plus.click(function() {
        var num = $count.val() * 1 || 0;
        setCount(num + 1);
        $product_quantity.find('.product-count').attr('value', num + 1);
    });

    $minus.click(function() {
        var num = $count.val() * 1 || 0;
        if (num <= 0) {
            setCount(0);
        } else {
            setCount(num - 1);
            $product_quantity.find('.product-count').attr('value', num - 1);
        }
    });

    $count.keyup(function() {
        var num = $count.val() * 1 || 0;
        setCount(num);
    });

    init();
}
