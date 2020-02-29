import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""响应按键"""
	if event.key == pygame.K_RIGHT:
		# 向右移动飞船
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		# 向左移动飞船
		ship.moving_left = True
	if event.key == pygame.K_UP:
		# 向上移动飞船
		ship.moving_up = True
	if event.key == pygame.K_DOWN:
		# 向下移动飞船
		ship.moving_down = True
	if event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	if event.key == pygame.K_q:
		sys.exit()

def check_keyup_events(event, ship):
	"""响应松开"""
	if event.key == pygame.K_RIGHT:
		# 停止右移飞船
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		# 停止左移飞船
		ship.moving_left = False
	if event.key == pygame.K_UP:
		# 停止上移飞船
		ship.moving_up = False
	if event.key == pygame.K_DOWN:
		# 停止下移飞船
		ship.moving_down = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	"""在玩家单机play按钮时开始新游戏"""
	button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_click and not stats.game_active:
		# 重置游戏速度
		ai_settings.initialize_dynamic_settings()
		# 隐藏光标
		pygame.mouse.set_visible(False)
		# 重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True
		# 重置记分牌图像：
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		# 清空外星人和子弹列表
		aliens.empty()
		bullets.empty()
		# 创建一行新外星人并让飞船居中
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
	# 创建一颗子弹并将其加入到编组bullets中
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	"""更新屏幕上的图像，并切换到新屏幕"""
	# 每次循环时都重绘屏幕
	screen.fill(ai_settings.bg_color)
	# 在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	# 绘制飞船
	ship.blitme()
	aliens.draw(screen)
	# 显示得分，最高分，等级
	sb.show_score()
	# 如果游戏非活动状态，绘制play按钮
	if not stats.game_active:
		play_button.draw_button()

	# 让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""更新子弹位置并消除到顶子弹"""
	# 更新子弹位置
	bullets.update()
	# 删除消失子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	# 检查是否有子弹击中外星人
	# 如果是，删除子弹和外星人
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	if len(aliens) == 0:
		# 删除现有子弹，加快速度，并新建一群外星人
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)
		stats.level += 1
		sb.prep_level()
		ship.center_ship()

def check_high_score(stats, sb):
	"""检查是否诞生新最高分"""
	if stats.high_score < stats.score:
		stats.high_score = stats.score
		sb.prep_high_score()

def create_fleet(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	# 创建一个外星人，并计算一行可容纳多少外星人
	# 外星人间距为外星人宽度
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
		alien.rect.height)
	# 创建外星人
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			# 创建一个外星人并将其加入当前行
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
		

def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_hight, alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_space_y = (ai_settings.screen_height - 
		(3 * alien_height) - ship_hight)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""创建一个外星人并将它放在当前行"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = 20 + alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
	"""有外星人到达边缘时采取相应措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""将整群外星人下移，并改变方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""响应被外星人撞到的飞船"""
	if stats.ship_left > 1:
		# ship left -1
		stats.ship_left -= 1

		# 更新记分牌
		sb.prep_ships()

		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建一群新外星人
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# 暂停
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""检查是否有外星人到达屏幕底端"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞船被撞到一样处理
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""更新外星人群位置"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	# 检测飞船与外星人间的碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
	# 检测是否到达屏幕底端
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)