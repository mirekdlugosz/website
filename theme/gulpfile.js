var gulp = require("gulp");
var sass = require("gulp-sass")(require("sass"));
var autoprefixer = require("gulp-autoprefixer")
var cleanCSS = require("gulp-clean-css");
var concat = require("gulp-concat");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");

// Compile SCSS
function css_compile() {
    return gulp.src([
        './src/scss/setup.scss',
        './src/scss/sanitize.scss',
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

// There used to be JavaScript minifier here
// Check git log if you ever need it back

// copy font files
function fonts() {
    return gulp.src([
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
exports.default = gulp.parallel(exports.css, exports.fonts, exports.images);

exports.dev = gulp.series(function() {
    gulp.watch('./src/img/**', { ignoreInitial: false }, exports.images);
    gulp.watch('./src/**/*.scss', { ignoreInitial: false }, exports.css);
});
