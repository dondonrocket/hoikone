/**
 * Directory – Directory & Listing Bootstrap Theme v. 2.0.2
 * Homepage: https://themes.getbootstrap.com/product/directory-directory-listing-bootstrap-4-theme/
 * Copyright 2022, Bootstrapious - https://bootstrapious.com
 */

"use strict";

$(function () {
    // ------------------------------------------------------- //
    //   Lightbox in galleries
    // ------------------------------------------------------ //

    $(".slider-gallery").each(function () {
        // the containers for all your galleries
        $(this).magnificPopup({
            delegate: "a", // the selector for gallery item
            type: "image",
            gallery: {
                enabled: true,
                tCounter: "", // markup of counter
            },
        });
    });

    $(".gallery").each(function () {
        // the containers for all your galleries
        $(this).magnificPopup({
            delegate: "a", // the selector for gallery item
            type: "image",
            gallery: {
                enabled: true,
            },
        });
    });

    // =====================================================
    //     Reset input
    // =====================================================

    $(".input-expand .form-control").on("focus", function () {
        $(this).parents(".input-expand").addClass("focus");
    });
    $(".input-expand .form-control").on("blur", function () {
        setTimeout(function () {
            $(".input-expand .form-control").parents(".input-expand").removeClass("focus");
        }, 333);
    });

    // =====================================================
    //      Detail slider
    // =====================================================

    var detailSlider = new Swiper(".detail-slider", {
        slidesPerView: 3,
        spaceBetween: 0,
        centeredSlides: true,
        loop: true,
        breakpoints: {
            991: {
                slidesPerView: 4,
            },
            565: {
                slidesPerView: 3,
            },
        },

        // If we need pagination
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            dynamicBullets: true,
        },

        // Navigation arrows
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
    });

    var bookingDetailSlider = new Swiper(".booking-detail-slider", {
        slidesPerView: 2,
        spaceBetween: 0,
        centeredSlides: true,
        loop: true,
        // If we need pagination
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            dynamicBullets: true,
        },

        // Navigation arrows
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
    });

    // =====================================================
    //      Init swipers automatically
    // =====================================================

    $(".swiper-init").each(function () {
        var slider = $(this),
            configuration = JSON.parse($(this).attr("data-swiper"));

        new Swiper(slider, configuration);
    });

    var homeSlider = new Swiper(".home-slider", {
        slidesPerView: 1,
        spaceBetween: 0,
        centeredSlides: true,
        loop: true,
        speed: 1500,
        parallax: true,
        /*
        autoplay: {
            delay: 5000,
        },
        */
        // If we need pagination
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            dynamicBullets: true,
        },
        // Navigation arrows
        navigation: {
            nextEl: "#homeNext",
            prevEl: "#homePrev",
        },
    });

    // =====================================================
    //      Items slider
    // =====================================================

    var itemsSlider = new Swiper(".items-slider", {
        slidesPerView: 4,
        spaceBetween: 20,
        loop: true,
        roundLengths: true,
        breakpoints: {
            1200: {
                slidesPerView: 3,
            },
            991: {
                slidesPerView: 2,
            },
            565: {
                slidesPerView: 1,
            },
        },

        // If we need pagination
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            dynamicBullets: true,
        },
    });

    var itemsSliderFull = new Swiper(".items-slider-full", {
        slidesPerView: 6,
        spaceBetween: 20,
        loop: true,
        roundLengths: true,
        breakpoints: {
            1600: {
                slidesPerView: 5,
            },
            1400: {
                slidesPerView: 4,
            },
            1200: {
                slidesPerView: 3,
            },
            991: {
                slidesPerView: 2,
            },
            565: {
                slidesPerView: 1,
            },
        },

        // If we need pagination
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            dynamicBullets: true,
        },
    });

    var guidesSlider = new Swiper(".guides-slider", {
        slidesPerView: 5,
        spaceBetween: 15,
        loop: true,
        roundLengths: true,
        breakpoints: {
            1200: {
                slidesPerView: 4,
            },
            991: {
                slidesPerView: 3,
            },
            768: {
                slidesPerView: 2,
            },
            400: {
                slidesPerView: 1,
            },
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            dynamicBullets: true,
        },
    });

    var brandsSlider = new Swiper(".brands-slider", {
        slidesPerView: 6,
        spaceBetween: 15,
        loop: true,
        roundLengths: true,
        breakpoints: {
            1200: {
                slidesPerView: 4,
            },
            991: {
                slidesPerView: 3,
            },
            768: {
                slidesPerView: 2,
            },
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            dynamicBullets: true,
        },
    });

    var swiper = new Swiper(".hero-slider", {
        effect: "fade",
        speed: 2000,
        allowTouchMove: false,
        autoplay: {
            delay: 10000,
        },
    });

    var instagramSlider = new Swiper(".instagram-slider", {
        slidesPerView: 16,
        breakpoints: {
            1900: {
                slidesPerView: 12,
            },
            1500: {
                slidesPerView: 10,
            },
            1200: {
                slidesPerView: 8,
            },
            991: {
                slidesPerView: 6,
            },
            768: {
                slidesPerView: 5,
            },
            576: {
                slidesPerView: 4,
            },
        },
    });

    var testimonialsSlider = new Swiper(".testimonials-slider", {
        slidesPerView: 2,
        spaceBetween: 20,
        loop: true,
        roundLengths: true,
        breakpoints: {
            1200: {
                slidesPerView: 3,
                spaceBetween: 0,
            },
            991: {
                slidesPerView: 2,
                spaceBetween: 0,
            },
            565: {
                slidesPerView: 1,
            },
        },

        // If we need pagination
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            dynamicBullets: true,
        },
    });

    // ------------------------------------------------------- //
    //   Increase/Decrease product amount
    // ------------------------------------------------------ //
    $(".btn-items-decrease").on("click", function () {
        var input = $(this).siblings(".input-items");
        if (parseInt(input.val(), 10) >= 1) {
            if (input.hasClass("input-items-greaterthan")) {
                input.val(parseInt(input.val(), 10) - 1 + "+");
            } else {
                input.val(parseInt(input.val(), 10) - 1);
            }
        }
    });

    $(".btn-items-increase").on("click", function () {
        var input = $(this).siblings(".input-items");
        if (input.hasClass("input-items-greaterthan")) {
            input.val(parseInt(input.val(), 10) + 1 + "+");
        } else {
            input.val(parseInt(input.val(), 10) + 1);
        }
    });

    // ------------------------------------------------------- //
    //   Scroll to top button
    // ------------------------------------------------------ //

    $(window).on("scroll", function () {
        if ($(window).scrollTop() >= 1500) {
            $("#scrollTop").fadeIn();
        } else {
            $("#scrollTop").fadeOut();
        }
    });

    $("#scrollTop").on("click", function () {
        $("html, body").animate(
            {
                scrollTop: 0,
            },
            1000
        );
    });

    // ------------------------------------------------------- //
    // Adding fade effect to dropdowns
    // ------------------------------------------------------ //

    $.fn.slideDropdownUp = function () {
        $(this).fadeIn().css("transform", "translateY(0)");
        return this;
    };
    $.fn.slideDropdownDown = function (movementAnimation) {
        if (movementAnimation) {
            $(this).fadeOut().css("transform", "translateY(30px)");
        } else {
            $(this).hide().css("transform", "translateY(30px)");
        }
        return this;
    };

    $(".navbar .dropdown").on("show.bs.dropdown", function (e) {
        $(this).find(".dropdown-menu").first().slideDropdownUp();
    });
    $(".navbar .dropdown").on("hide.bs.dropdown", function (e) {
        var movementAnimation = true;

        // if on mobile or navigation to another page
        if ($(window).width() < 992 || (e.clickEvent && e.clickEvent.target.tagName.toLowerCase() === "a")) {
            movementAnimation = false;
        }

        $(this).find(".dropdown-menu").first().slideDropdownDown(movementAnimation);
    });

    // ------------------------------------------------------- //
    //    Collapse button control (used for more/less filters)
    // ------------------------------------------------------ //

    $(".btn-collapse").each(function () {
        var button = $(this),
            collapseId = button.attr("data-bs-target");

        if ($(collapseId).length) {
            var collapseElement = $(collapseId);

            $(collapseElement).on("hide.bs.collapse", function () {
                button.text(button.attr("data-collapsed-text"));
            });

            $(collapseElement).on("show.bs.collapse", function () {
                button.text(button.attr("data-expanded-text"));
            });
        }
    });

    // ------------------------------------------------------- //
    //   Bootstrap tooltips
    // ------------------------------------------------------- //

    $('[data-bs-toggle="tooltip"]').tooltip();

    // ------------------------------------------------------- //
    //   Smooth Scroll
    // ------------------------------------------------------- //

    var smoothScroll = new SmoothScroll("a[data-smooth-scroll]", {
        offset: 80,
    });

    // ------------------------------------------------------- //
    //   Object Fit Images
    // ------------------------------------------------------- //

    objectFitImages();
});

// ------------------------------------------------------- //
//   検索機能追加
// ------------------------------------------------------ //

//document.getElementById('search').addEventListener('submit', function (event) {
//    event.preventDefault();
//    var searchKeyword = document.getElementById('search-search').value;

// Django REST FrameworkのAPIエンドポイントに検索リクエストを送信
//    var apiUrl = '/hoikone/nurseries/?search=' + encodeURIComponent(searchKeyword);
//    axios.get(apiUrl)
//        .then(function (response) {
//            // レスポンスデータの処理
//            var nurseries = response.data;
//            displaySearchResults(nurseries);
//        })
//        .catch(function (error) {
//            console.error('検索リクエストの送信に失敗しました: ' + error);
//        });
//});

//function displaySearchResults(nurseries) {
//    var resultsContainer = document.getElementById('search-results');
//    resultsContainer.innerHTML = '';

// 検索結果を表示
//    nurseries.forEach(function (nursery) {
//        var nurseryItem = document.createElement('div');
//        nurseryItem.textContent = nursery.name;
//        resultsContainer.appendChild(nurseryItem);
//    });
//}
// ------------------------------------------------------- //
//   スクロールするまでヘッダーを非表示
// ------------------------------------------------------ //
const header = document.querySelector('header');
const headerLinks = document.querySelectorAll('.header-link');

function updateHeaderVisibility() {
    const scrollPosition = window.scrollY;
    if (scrollPosition > 50) {
        header.classList.add('visible');
        // スクロール位置が50より大きい場合はリンクを有効化
        headerLinks.forEach(link => {
            link.style.pointerEvents = 'auto';
        });
    } else {
        header.classList.remove('visible');
        // スクロール位置が50以下の場合はリンクを無効化
        headerLinks.forEach(link => {
            link.style.pointerEvents = 'none';
        });
    }
}

window.addEventListener('scroll', () => {
    updateHeaderVisibility();
});

// 初期表示時にヘッダーの状態を更新
updateHeaderVisibility();

// ------------------------------------------------------- //
//   スライダーのキーワード検索
// ------------------------------------------------------ //
// 

document.querySelectorAll('.swiper-slide').forEach(function (card) {
    card.addEventListener('click', function (event) {
        // クリックされた項目の文字列を取得
        var keyword = card.querySelector('.card-title').innerText;

        // Django RESTフレームワークのAPIエンドポイントに検索リクエストを送信
        // ここでAjaxリクエストを使用してバックエンドと通信します
        // 例：axiosやfetch APIを使ってGETリクエストを送信し、検索結果を受け取る
        axios.get('hoikone/v1/nursery-list/', {
            params: {
                query: keyword
            }
        })
            .then(function (response) {
                // 検索結果を取得して、テンプレートに表示する処理を行う
                // response.dataに検索結果が含まれると仮定します
                var searchResults = response.data;
                // テンプレートに検索結果を表示する処理を行う
                // 例：searchResultsをテンプレートの適切な部分に表示する

                // 通常のページ遷移を実行
                window.location.href = 'hoikone/v1/nursery-list/?query=' + encodeURIComponent(keyword);
            })
            .catch(function (error) {
                // エラーハンドリングを行う
            });
    });
});

// ------------------------------------------------------- //
//   プレビュー表示
// ------------------------------------------------------ //
// 
function updateImagePreview(input, previewId) {
    var file = input.files[0];
    var imgPreview = document.getElementById(previewId);

    // 画像が選択された場合のみプレビューを表示する
    if (file) {
        var reader = new FileReader();
        reader.onload = function (e) {
            imgPreview.src = e.target.result;
        }
        reader.readAsDataURL(file);
    } else {
        imgPreview.src = '';
    }
}

var formFeatureImage = document.getElementById('form_feature_image');
if (formFeatureImage) {
    formFeatureImage.addEventListener('change', function (e) {
        updateImagePreview(e.target, 'feature_image_preview');
    });
}

var formExperienceImage = document.getElementById('form_experience_image');
if (formExperienceImage) {
    formExperienceImage.addEventListener('change', function (e) {
        updateImagePreview(e.target, 'experience_image_preview');
    });
}

var formImage = document.getElementById('form_image');
if (formImage) {
    formImage.addEventListener('change', function (e) {
        updateImagePreview(e.target, 'image_preview');
    });
}


//document.getElementById('form_feature_image').addEventListener('change', function (e) {
//    updateImagePreview(e.target, 'feature_image_preview');
//});

//document.getElementById('form_experience_image').addEventListener('change', function (e) {
//    updateImagePreview(e.target, 'experience_image_preview');
//});

//document.getElementById('form_image').addEventListener('change', function (e) {
//    updateImagePreview(e.target, 'image_preview');
//});


