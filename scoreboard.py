import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	"""显示得分信息的类"""

	def __init__(self, ai_settings, screen, stats):
		self.ai_settings = ai_settings
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.stats = stats

		# 显示得分信息时使用的字体设置
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 36)

		# 准备初始得分图像和最高分图像
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		"""将得分转换为一幅渲染的图像"""
		rounded_score = int(round(self.stats.score, -1))
		score_str = "SCORE: " + "{:,}".format(rounded_score)
		
		self.score_image = self.font.render(score_str, True, self.text_color,
			self.ai_settings.bg_color)

		# 将得分放在屏幕右上角
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = self.screen_rect.top

	def prep_high_score(self):
		"""将最高分转换为渲染图像"""
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "HIGH SCORE: " + "{:,}".format(high_score)
		
		self.high_score_image = self.font.render(high_score_str, True, self.text_color,
			self.ai_settings.bg_color)

		# 将最高分放在屏幕中间顶部
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.screen_rect.top

	def prep_level(self):
		"""将等级转换为渲染图像"""
		level = self.stats.level
		level_str = "LEVEL: " + str(level)
		self.level_image = self.font.render(level_str, True, self.text_color,
			self.ai_settings.bg_color)
		# 将等级放在屏幕右边顶部
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		"""显示还剩下多少飞船"""
		self.ships = Group()
		for ship_number in range(self.stats.ship_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * (ship.rect.width + 10)
			ship.rect.y = 0
			self.ships.add(ship)

	def show_score(self):
		"""在屏幕上显示得分和最高分"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		# 绘制剩余飞船
		self.ships.draw(self.screen)

