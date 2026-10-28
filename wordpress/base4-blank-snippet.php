/**
 * BASE4 Blank page template
 *
 * Adds a "BASE4 Blank" page template that shows only the page content:
 * no theme header, footer or sidebar, and no theme stylesheets. The page code
 * is output exactly as published (no content filters), so its scripts run intact.
 * Password-protected pages still show the password form.
 * WordPress essentials (wp_head / wp_footer) still load, so Yoast SEO tags,
 * analytics and plugins keep working.
 *
 * Paste into Code Snippets (Snippets -> Add New), set to "Run snippet everywhere",
 * then Save and Activate. Deactivating the snippet puts the pages back on the
 * normal theme layout.
 */

// 1. Make the template selectable (and settable through the REST API).
add_filter( 'theme_page_templates', function ( $templates ) {
	$templates['base4-blank'] = 'BASE4 Blank (no theme header/footer)';
	return $templates;
} );

function base4_is_blank_page() {
	return is_singular( 'page' ) && get_page_template_slug( get_queried_object_id() ) === 'base4-blank';
}

// 2. Drop the theme's own CSS/JS on these pages so they don't clash with the page design.
add_action( 'wp_enqueue_scripts', function () {
	if ( ! base4_is_blank_page() ) {
		return;
	}
	$theme_urls = array_unique( array( get_template_directory_uri(), get_stylesheet_directory_uri() ) );
	foreach ( array( wp_styles(), wp_scripts() ) as $deps ) {
		foreach ( $deps->queue as $handle ) {
			$src = isset( $deps->registered[ $handle ] ) ? (string) $deps->registered[ $handle ]->src : '';
			foreach ( $theme_urls as $url ) {
				if ( $src && strpos( $src, $url ) === 0 ) {
					$deps instanceof WP_Styles ? wp_dequeue_style( $handle ) : wp_dequeue_script( $handle );
				}
			}
		}
	}
}, 999 );

// 3. Render only the page content inside a minimal HTML document.
add_action( 'template_redirect', function () {
	if ( ! base4_is_blank_page() ) {
		return;
	}
	?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class( 'base4-blank' ); ?>>
<?php
	if ( function_exists( 'wp_body_open' ) ) {
		wp_body_open();
	}
	$base4_post = get_queried_object();
	if ( post_password_required( $base4_post ) ) {
		echo get_the_password_form( $base4_post );
	} else {
		// Output the page code exactly as published. WordPress content filters
		// (smart quotes, image attributes, shortcodes) rewrite markup inside the
		// page's JavaScript and break it, so they are skipped on these pages.
		echo $base4_post->post_content; // phpcs:ignore WordPress.Security.EscapeOutput -- admin-published page code
	}
	wp_footer();
?>
</body>
</html>
<?php
	exit;
} );
