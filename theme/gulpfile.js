var gulp = require("gulp");
var sass = require("gulp-sass");
var autoprefixer = require("gulp-autoprefixer")
var cleanCSS = require("gulp-clean-css");
var concat = require("gulp-concat");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");

// Compile SCSS
function css_compile() {
    return gulp.src([
        './src/scss/variables.scss',
        './src/scss/bootstrap.scss',
        './src/scss/fontawesome.scss',
        './src/scss/pygments.scss',
        './vendor/Merriweather/style.scss',
        './src/scss/style.scss',
    ])
        .pipe(concat('style.scss'))
        .pipe(sass.sync({
            outputStyle: 'expanded'
        }).on('error', sass.logError))
        .pipe(autoprefixer('last 2 versions'))
        .pipe(gulp.dest('./static/css'))
}

// Minify CSS
function css_minify() {
    return gulp.src([
        './static/css/**/*.css',
        '!./static/css/**/*.min.css'
    ])
        .pipe(concat('style.css'))
        .pipe(cleanCSS())
        .pipe(rename({
            suffix: '.min'
        }))
        .pipe(gulp.dest('./static/css'));
}

// CSS
exports.css = gulp.series(css_compile, css_minify);

// Minify JavaScript
function js_minify() {
    return gulp.src([
        './node_modules/bootstrap.native/dist/bootstrap-native.min.js',
        './src/js/*.js'
    ])
        .pipe(concat('script.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./static/js'));
}

// JS
exports.js = gulp.series(js_minify);

// copy FontAwesome font files
function fonts() {
    return gulp.src([
        './node_modules/@fortawesome/fontawesome-free/webfonts/*',
        './vendor/Merriweather/*',
        '!./vendor/Merriweather/style.scss'
    ])
        .pipe(gulp.dest('./static/fonts'));
}

exports.fonts = fonts;

// copy images
function images() {
    return gulp.src([
        './src/img/*'
    ])
        .pipe(gulp.dest('./static/img'));
}

exports.images = images;

// Default task
exports.default = gulp.parallel(exports.css, exports.js, exports.fonts, exports.images);

exports.dev = gulp.series(function() {
    gulp.watch('./src/img/**', { ignoreInitial: false }, exports.images);
    gulp.watch('./src/**/*.scss', { ignoreInitial: false }, exports.css);
    gulp.watch('./src/**/*.js', { ignoreInitial: false }, exports.js);
});
