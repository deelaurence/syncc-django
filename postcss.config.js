module.exports = {
    plugins: [
        require('@fullhuman/postcss-purgecss')({
            content: ['./**/*.html'],
            defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
        }),
    ],
};
