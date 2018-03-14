import os
import random
import sys
import time

import pygame
import pygame.sprite
from pygame.event import EventType
from pygame.sprite import Group

from alien import Alien
from bullets import Bullet
from game_items import GameItems
from game_stats import GameStats
from settings import Settings
from ship import Ship


def check_events(ai_settings: Settings, stats: GameStats, game_items: GameItems):
    """Responds to keypresses and mouse events."""

    # Watch for keyboard and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game(stats)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, game_items)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, game_items.ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mousedown_events(ai_settings, stats, game_items)


def quit_game(stats: GameStats):
    """Saves the highscore and exits game"""
    filename = os.path.join('.', 'save/highscore.txt')
    with open(filename, 'w') as f:
        f.write(str(stats.high_score))
    sys.exit()


def update_screen(ai_settings: Settings, stats: GameStats, game_items: GameItems):
    """Update images on the screen and flip to the new screen."""

    # Redraw the screen during each pass through the loop.
    game_items.screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in game_items.bullets.sprites():
        bullet.draw_bullet()

    # Draw ship.
    game_items.ship.blitme()

    # Draw alien.
    game_items.aliens.draw(game_items.screen)

    # Display scorecard.
    game_items.sb.show_score()

    # Draw button.
    if not stats.game_active:
        game_items.play_button.draw_button()

    # game_items.restart_button.draw_button()
    # game_items.cancel_button.draw_button()
    # Make the most recent screen visible.
    pygame.display.flip()


def check_keydown_events(event: EventType, ai_settings: Settings
                         , stats: GameStats, game_items: GameItems):
    if event.key == pygame.K_RIGHT:
        # Move ship to the right.
        game_items.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move ship to the left.
        game_items.ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, game_items)

    elif event.key == pygame.K_q:
        quit_game(stats)


def check_keyup_events(event: EventType, ship: Ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_mousedown_events(ai_settings: Settings, stats: GameStats, game_items: GameItems):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    check_play_button(ai_settings, stats, game_items, mouse_x, mouse_y)


def check_play_button(ai_settings: Settings, stats: GameStats, game_items: GameItems
                      , mouse_x: int, mouse_y: int):
    """Start a new game when the player clicks play_button."""
    button_clicked = game_items.play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Resets game statistics.
        stats.reset_stats()
        stats.game_active = True
        ai_settings.initialize_dynamic_settings()

        # Reset scoreboard.
        game_items.sb.prep_score()
        game_items.sb.prep_high_score()
        game_items.sb.prep_level()
        game_items.sb.prep_ships()

        # Empty bullets and aliens group.
        game_items.bullets.empty()
        game_items.aliens.empty()

        # Create new fleet and center the ship.
        create_fleet(ai_settings, game_items)
        game_items.ship.center_ship()

        # Hide mouse.
        pygame.mouse.set_visible(False)


def update_bullets(ai_settings: Settings, stats: GameStats, game_items: GameItems):
    game_items.bullets.update(stats)
    # Get rid of bullets that have disappeared.
    for bullet in game_items.bullets.copy():
        if bullet.rect.bottom <= 0:
            game_items.bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, stats, game_items)


def check_bullet_alien_collision(ai_settings: Settings, stats: GameStats, game_items: GameItems):
    # Get rid of bullet and aliens that have collided.
    collision = pygame.sprite.groupcollide(game_items.bullets, game_items.aliens, True, True)
    if collision:
        for aliens_hit_list in collision.values():
            stats.score += ai_settings.alien_points * len(aliens_hit_list)
            game_items.sb.prep_score()
        check_high_score(stats, game_items)

    # Create new fleet after fleet is empty.
    if len(game_items.aliens.sprites()) == 0:
        game_items.bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        game_items.sb.prep_level()
        create_fleet(ai_settings, game_items)


def update_aliens(ai_settings: Settings, stats: GameStats, game_items: GameItems):
    """Updates position for each alien."""
    check_fleet_edges(ai_settings, game_items.aliens)
    game_items.aliens.update(stats)

    # Collision between ship and aliens.
    if pygame.sprite.spritecollideany(game_items.ship, game_items.aliens):
        ship_hit(ai_settings, stats, game_items)
    check_aliens_bottom(ai_settings, stats, game_items)


def fire_bullets(ai_settings: Settings, game_items: GameItems):
    """Fires a bullet if limit not reached."""

    # Create a new bullet and add it to the bullets group.
    if len(game_items.bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, game_items.screen, game_items.ship)
        game_items.bullets.add(new_bullet)


def create_fleet(ai_settings: Settings, game_items: GameItems):
    """Create a full fleet of aliens."""

    alien = Alien(ai_settings, game_items.screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, game_items.ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, game_items, alien_number, row_number)


def create_alien(ai_settings: Settings, game_items: GameItems
                 , alien_number: int, row_number: int):
    RAND_NO_X = random.randint(-ai_settings.alien_random_x, ai_settings.alien_random_x)
    RAND_NO_Y = random.randint(-ai_settings.alien_random_y, ai_settings.alien_random_y)

    # Change directions to default.
    ai_settings.set_default_alien_directions()

    alien = Alien(ai_settings, game_items.screen)
    alien_width = alien.rect.width
    alien.x = alien_width + (ai_settings.alien_density_factor_x * alien_width * alien_number) + RAND_NO_X
    alien.rect.x = alien.x
    alien_height = alien.rect.height
    alien.y = 100 + (ai_settings.alien_density_factor_y * alien_height * row_number) + RAND_NO_Y

    alien.rect.y = alien.y
    alien.drop_dist = alien.y + ai_settings.alien_drop_dist

    game_items.aliens.add(alien)


def get_number_aliens_x(ai_settings: Settings, alien_width: int):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (ai_settings.alien_density_factor_x * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings: Settings, ship_height: int, alien_height: int):
    available_space_y = (ai_settings.screen_height - alien_height * ai_settings.alien_ship_dist_factor
                         - alien_height - ship_height)
    number_rows = int(available_space_y / (alien_height * ai_settings.alien_density_factor_y))
    return number_rows


def change_fleet_directions(ai_settings: Settings, aliens: Group, direction: int):
    """Drops down the fleet and change the direction."""
    for alien in aliens:
        if alien.y <= alien.drop_dist:
            ai_settings.alien_direction_y = 1
            ai_settings.alien_direction_x = 0
        else:
            ai_settings.alien_direction_y = 0
            ai_settings.alien_direction_x = direction


def check_fleet_edges(ai_settings: Settings, aliens: Group):
    """Responds appropriately when any alien reaches edge."""
    for alien in aliens:
        if alien.check_edges('left'):
            change_fleet_directions(ai_settings, aliens, direction=+1)
            break
        elif alien.check_edges('right'):
            change_fleet_directions(ai_settings, aliens, direction=-1)
            break


def ship_hit(ai_settings: Settings, stats: GameStats, game_items: GameItems):
    """Responds to ship being hit by an alien."""

    if stats.ships_left > 0:

        # Decrement ships left.
        stats.ships_left -= 1

        # Updates scorecard.
        game_items.sb.prep_ships()

        # Empty bullets and aliens.
        game_items.bullets.empty()
        game_items.aliens.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, game_items)
        game_items.ship.center_ship()

        # Pause.
        time.sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings: Settings, stats: GameStats, game_items: GameItems):
    """Check if aliens reached bottom of the screen."""

    for alien in game_items.aliens:
        if alien.rect.bottom >= alien.screen_rect.bottom:
            # Behave like ship_hit.
            ship_hit(ai_settings, stats, game_items)
            break


def check_high_score(stats: GameStats, game_items: GameItems):
    """Check for a high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        game_items.sb.prep_high_score()
