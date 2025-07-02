/**
 * Prodamin JavaScript Functions
 * منصة تخطيط وإنجاز مدعومة بالذكاء الاصطناعي
 *
 * @format
 */

// تهيئة التطبيق
$(document).ready(function () {
  initializeProdamin();
});

function initializeProdamin() {
  // تهيئة المكونات الأساسية
  setupCSRF();
  setupAnimations();
  setupTooltips();
  setupCounters();
  setupFormValidation();
  setupNotifications();

  console.log("✅ Prodamin initialized successfully!");
}

// إعداد CSRF Token
function setupCSRF() {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  // إعداد AJAX headers
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  window.csrftoken = csrftoken;
}

// إعداد الأنيميشن
function setupAnimations() {
  // Fade in للعناصر
  $(".fade-in").css("opacity", "0").animate({ opacity: 1 }, 800);

  // تأثير slide up للكروت
  $(".card").each(function (index) {
    $(this)
      .delay(index * 100)
      .queue(function () {
        $(this).addClass("slide-up").dequeue();
      });
  });

  // إخفاء التنبيهات تلقائياً
  setTimeout(function () {
    $(".alert").fadeOut("slow");
  }, 5000);
}

// إعداد Tooltips
function setupTooltips() {
  if (typeof bootstrap !== "undefined") {
    var tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
}

// إعداد العدادات المتحركة
function setupCounters() {
  $(".stats-number").each(function () {
    const $this = $(this);
    const countTo = parseInt($this.text()) || 0;

    $({ countNum: 0 }).animate(
      {
        countNum: countTo,
      },
      {
        duration: 2000,
        easing: "swing",
        step: function () {
          $this.text(Math.floor(this.countNum));
        },
        complete: function () {
          $this.text(countTo);
        },
      }
    );
  });
}

// إعداد التحقق من النماذج
function setupFormValidation() {
  // التحقق من قوة كلمة المرور
  $("#password1").on("input", function () {
    checkPasswordStrength($(this).val());
  });

  // التحقق من تطابق كلمات المرور
  $("#password2").on("input", function () {
    checkPasswordMatch();
  });

  // التحقق من صحة البريد الإلكتروني
  $('input[type="email"]').on("blur", function () {
    validateEmail($(this));
  });
}

// فحص قوة كلمة المرور
function checkPasswordStrength(password) {
  const strengthBar = $("#passwordStrength");
  const strengthText = $("#strengthText");

  if (!strengthBar.length) return;

  let strength = 0;
  let text = "";
  let color = "";

  // معايير القوة
  if (password.length >= 8) strength += 25;
  if (/[a-z]/.test(password)) strength += 25;
  if (/[A-Z]/.test(password)) strength += 25;
  if (/[0-9]/.test(password)) strength += 25;

  // تحديد النص واللون
  if (strength <= 25) {
    text = "ضعيفة";
    color = "bg-danger";
  } else if (strength <= 50) {
    text = "متوسطة";
    color = "bg-warning";
  } else if (strength <= 75) {
    text = "جيدة";
    color = "bg-info";
  } else {
    text = "قوية";
    color = "bg-success";
  }

  strengthBar
    .css("width", strength + "%")
    .removeClass()
    .addClass("progress-bar " + color);
  strengthText.text(text);
}

// فحص تطابق كلمات المرور
function checkPasswordMatch() {
  const password1 = $("#password1").val();
  const password2 = $("#password2").val();
  const matchText = $("#passwordMatch");

  if (!matchText.length || !password2) return;

  if (password1 === password2) {
    matchText
      .html('<i class="fas fa-check text-success"></i> كلمات المرور متطابقة')
      .removeClass()
      .addClass("form-text text-success");
  } else {
    matchText
      .html('<i class="fas fa-times text-danger"></i> كلمات المرور غير متطابقة')
      .removeClass()
      .addClass("form-text text-danger");
  }
}

// التحقق من صحة البريد الإلكتروني
function validateEmail(input) {
  const email = input.val();
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (email && !emailRegex.test(email)) {
    input.addClass("is-invalid");
    showNotification("البريد الإلكتروني غير صحيح", "error");
  } else {
    input.removeClass("is-invalid");
  }
}

// إعداد النوتيفيكيشن
function setupNotifications() {
  // إنشاء container للإشعارات إذا لم يكن موجوداً
  if (!$("#notifications-container").length) {
    $("body").prepend(
      '<div id="notifications-container" style="position: fixed; top: 20px; right: 20px; z-index: 9999;"></div>'
    );
  }
}

// إظهار إشعار
function showNotification(message, type = "info", duration = 5000) {
  const types = {
    success: "alert-success",
    error: "alert-danger",
    warning: "alert-warning",
    info: "alert-info",
  };

  const icons = {
    success: "fa-check-circle",
    error: "fa-exclamation-circle",
    warning: "fa-exclamation-triangle",
    info: "fa-info-circle",
  };

  const notification = $(`
        <div class="alert ${types[type]} alert-dismissible fade show" role="alert" style="margin-bottom: 10px; min-width: 300px;">
            <i class="fas ${icons[type]} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);

  $("#notifications-container").append(notification);

  // إزالة تلقائية
  setTimeout(() => {
    notification.fadeOut(() => notification.remove());
  }, duration);
}

// وظائف المهام
const TaskManager = {
  // تحديث حالة المهمة
  updateStatus: function (taskId, status) {
    return $.post(`/tasks/${taskId}/update-status/`, {
      status: status,
      csrfmiddlewaretoken: window.csrftoken,
    });
  },

  // إضافة ملاحظة
  addNote: function (taskId, content) {
    return $.post(`/tasks/${taskId}/add-note/`, {
      content: content,
      csrfmiddlewaretoken: window.csrftoken,
    });
  },

  // حذف مهمة
  deleteTask: function (taskId) {
    if (confirm("هل أنت متأكد من حذف هذه المهمة؟")) {
      return $.post(`/tasks/${taskId}/delete/`, {
        csrfmiddlewaretoken: window.csrftoken,
      });
    }
    return Promise.reject("تم إلغاء الحذف");
  },
};

// وظائف المكافآت
const RewardManager = {
  // المطالبة بمكافأة
  claimReward: function (rewardId) {
    return $.post(`/rewards/claim/${rewardId}/`, {
      csrfmiddlewaretoken: window.csrftoken,
    });
  },

  // شراء مكافأة
  purchaseReward: function (rewardTypeId) {
    return $.post(`/rewards/purchase/${rewardTypeId}/`, {
      csrfmiddlewaretoken: window.csrftoken,
    });
  },
};

// وظائف مساعدة
const Utils = {
  // تنسيق التاريخ
  formatDate: function (date) {
    const options = {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    };
    return new Date(date).toLocaleDateString("ar-SA", options);
  },

  // تنسيق الأرقام
  formatNumber: function (number) {
    return new Intl.NumberFormat("ar-SA").format(number);
  },

  // حساب الوقت المنقضي
  timeAgo: function (date) {
    const now = new Date();
    const past = new Date(date);
    const diffInSeconds = Math.floor((now - past) / 1000);

    if (diffInSeconds < 60) return "منذ لحظات";
    if (diffInSeconds < 3600)
      return `منذ ${Math.floor(diffInSeconds / 60)} دقيقة`;
    if (diffInSeconds < 86400)
      return `منذ ${Math.floor(diffInSeconds / 3600)} ساعة`;
    return `منذ ${Math.floor(diffInSeconds / 86400)} يوم`;
  },

  // تحديث نقاط المستخدم
  updateUserPoints: function (points) {
    $("#user-points").text(this.formatNumber(points));

    // تأثير بصري
    $("#user-points").addClass("glow");
    setTimeout(() => {
      $("#user-points").removeClass("glow");
    }, 1000);
  },
};

// إعداد أحداث المهام
$(document).on("click", ".claim-reward", function () {
  const rewardId = $(this).data("reward-id");
  const button = $(this);

  button
    .prop("disabled", true)
    .html('<i class="fas fa-spinner fa-spin"></i> جاري التحميل...');

  RewardManager.claimReward(rewardId)
    .done(function (data) {
      if (data.success) {
        button.closest(".card").fadeOut();
        Utils.updateUserPoints(data.remaining_points);
        showNotification(data.message, "success");
      } else {
        showNotification(data.message, "error");
        button.prop("disabled", false).html("احصل عليها");
      }
    })
    .fail(function () {
      showNotification("حدث خطأ، يرجى المحاولة مرة أخرى.", "error");
      button.prop("disabled", false).html("احصل عليها");
    });
});

// تحديث حالة المهمة
$(document).on("change", ".task-status-select", function () {
  const taskId = $(this).data("task-id");
  const newStatus = $(this).val();
  const row = $(this).closest("tr");

  TaskManager.updateStatus(taskId, newStatus)
    .done(function (data) {
      if (data.success) {
        showNotification(data.message, "success");

        // تحديث التصميم
        row.removeClass().addClass(`task-${newStatus}`);

        if (newStatus === "completed") {
          row.addClass("table-success");
        }
      } else {
        showNotification(data.message, "error");
      }
    })
    .fail(function () {
      showNotification("فشل في تحديث المهمة", "error");
    });
});

// البحث المباشر
let searchTimeout;
$(document).on("input", ".search-input", function () {
  clearTimeout(searchTimeout);
  const query = $(this).val();

  searchTimeout = setTimeout(() => {
    if (query.length >= 2) {
      performSearch(query);
    } else if (query.length === 0) {
      clearSearchResults();
    }
  }, 300);
});

function performSearch(query) {
  // تنفيذ البحث (حسب السياق)
  console.log("Searching for:", query);
}

function clearSearchResults() {
  // مسح نتائج البحث
  console.log("Clearing search results");
}

// اشتراك النشرة البريدية
$(document).on("submit", "#newsletter-form", function (e) {
  e.preventDefault();

  const email = $(this).find('input[type="email"]').val();
  const submitBtn = $(this).find('button[type="submit"]');

  submitBtn
    .prop("disabled", true)
    .html('<i class="fas fa-spinner fa-spin"></i> جاري الاشتراك...');

  $.post("/subscribe-newsletter/", {
    email: email,
    csrfmiddlewaretoken: window.csrftoken,
  })
    .done(function (data) {
      if (data.success) {
        showNotification(data.message, "success");
        $("#newsletter-form")[0].reset();
      } else {
        showNotification(data.message, "error");
      }
    })
    .fail(function () {
      showNotification("حدث خطأ، يرجى المحاولة مرة أخرى.", "error");
    })
    .always(function () {
      submitBtn.prop("disabled", false).html("اشترك");
    });
});

// تحميل شعار عشوائي
function getRandomSlogan() {
  $.get("/get-random-slogan/")
    .done(function (data) {
      if (data.success) {
        const slogan = data.slogan;
        const html = `
                    <div class="alert alert-light border-0 mb-4 fade-in">
                        <i class="fas fa-quote-left text-accent"></i>
                        <em class="text-dark">${slogan.text_ar}</em>
                        ${
                          slogan.author
                            ? `<small class="d-block text-muted mt-1">- ${slogan.author}</small>`
                            : ""
                        }
                    </div>
                `;

        $(".hero-section .alert").fadeOut(300, function () {
          $(this).replaceWith(html);
        });
      }
    })
    .fail(function () {
      showNotification("فشل في تحميل شعار جديد", "error");
    });
}

// تهيئة الرسوم البيانية
function initializeCharts() {
  if (typeof Chart !== "undefined") {
    // إعدادات افتراضية للرسوم البيانية
    Chart.defaults.font.family = "Tajawal";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = "#212121";
  }
}

// تصدير الوظائف للاستخدام العام
window.ProdaminJS = {
  TaskManager,
  RewardManager,
  Utils,
  showNotification,
  getRandomSlogan,
  initializeCharts,
};

// إضافة تأثيرات بصرية للتفاعل
$(document).on("mouseenter", ".clickable", function () {
  $(this).addClass("shadow-medium");
});

$(document).on("mouseleave", ".clickable", function () {
  $(this).removeClass("shadow-medium");
});

// تحسين الأداء - تأجيل تحميل الصور
$(document).ready(function () {
  $("img[data-src]").each(function () {
    const img = $(this);
    const src = img.attr("data-src");

    if (src) {
      img.attr("src", src).removeAttr("data-src");
    }
  });
});

console.log("🚀 Prodamin JavaScript loaded successfully!");
