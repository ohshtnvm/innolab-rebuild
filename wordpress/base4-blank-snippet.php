/**
 * BASE4 page templates
 *
 * Adds two page templates for the rebuilt pages (Home, About, Hospitality, Multifamily):
 *
 *  - "BASE4 Blank": only the page content. No theme header, footer or sidebar,
 *    and no theme stylesheets.
 *  - "BASE4 with site header": the site's normal WordPress header and menu on top,
 *    then the page content. The page's own header bar and the theme footer are
 *    hidden, so there is one menu and one footer.
 *
 * In both, the page code is output exactly as published (no content filters), so its
 * scripts run intact, and password-protected pages still show the password form.
 * WordPress essentials (wp_head / wp_footer) still load, so Yoast SEO tags,
 * analytics and plugins keep working.
 *
 * Paste into WPCode / Code Snippets as a PHP snippet, "Run Everywhere", then Save and
 * Activate. Deactivating the snippet puts the pages back on the normal theme layout.
 */

// 1. Make the templates selectable (and settable through the REST API).
add_filter( 'theme_page_templates', function ( $templates ) {
	$templates['base4-blank']  = 'BASE4 Blank (no theme header/footer)';
	$templates['base4-themed'] = 'BASE4 with site header';
	return $templates;
} );

function base4_template() {
	if ( ! is_singular( 'page' ) ) {
		return '';
	}
	$slug = get_page_template_slug( get_queried_object_id() );
	return in_array( $slug, array( 'base4-blank', 'base4-themed' ), true ) ? $slug : '';
}

function base4_print_page_content() {
	$post = get_queried_object();
	if ( post_password_required( $post ) ) {
		echo get_the_password_form( $post );
		return;
	}
	// Output the page code exactly as published. WordPress content filters
	// (smart quotes, image attributes, shortcodes) rewrite markup inside the
	// page's JavaScript and break it, so they are skipped on these pages.
	echo $post->post_content; // phpcs:ignore WordPress.Security.EscapeOutput -- admin-published page code
}

// 2. Blank template only: drop the theme's own CSS/JS so it doesn't clash with the page design.
add_action( 'wp_enqueue_scripts', function () {
	if ( base4_template() !== 'base4-blank' ) {
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

// 3. Body class used by the header-template styles below.
add_filter( 'body_class', function ( $classes ) {
	$t = base4_template();
	if ( $t ) {
		$classes[] = $t;
	}
	return $classes;
} );

// 4. Render the page.
add_action( 'template_redirect', function () {
	$t = base4_template();
	if ( ! $t ) {
		return;
	}

	if ( $t === 'base4-themed' ) {
		get_header(); // the site's normal header and menu
		?>
<style>
body.base4-themed #b4-header{display:none}
body.base4-themed .znpb-footer-smart-area{display:none}
body.base4-themed #b4-page{padding-top:var(--b4-top,0px)}
</style>
<script>
(function(){
	function offset(){
		var h=document.querySelector('#header.site-header'), p=document.getElementById('b4-page');
		if(!h||!p){return;}
		var pos=getComputedStyle(h).position;
		p.style.setProperty('--b4-top',(pos==='absolute'||pos==='fixed')?h.offsetHeight+'px':'0px');
	}
	offset();
	document.addEventListener('DOMContentLoaded',offset);
	window.addEventListener('load',offset);
	window.addEventListener('resize',offset);
})();
</script>
		<?php
		base4_print_page_content();
		get_footer();
		exit;
	}

	?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php
	if ( function_exists( 'wp_body_open' ) ) {
		wp_body_open();
	}
	base4_print_page_content();
	wp_footer();
?>
</body>
</html>
<?php
	exit;
} );
