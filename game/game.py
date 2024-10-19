import pygame
from grids import BaseGrid, Coordinate
from game.constants import *
from constants import *
import pygame_gui as gui
from conditions.borders import *
from game.color_gen import ColorEngine

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.manager = gui.UIManager((WINDOW_SIZE[0], WINDOW_SIZE[1]))
        pygame.display.set_caption("Cellamata")
        self.clock = pygame.time.Clock()

        # Create the grid
        self.grid = BaseGrid(GRID_WIDTH, GRID_HEIGHT, BaseBorder(GRID_WIDTH, GRID_HEIGHT))
        self.color_engine = ColorEngine()
        
        # Initialize the machines
        self.machines = []
        self.running = True
        self.game_over = False
        self.end_machine = None
        self.speed = 60  # Default speed in ticks per secondt
        self.paused = False
    
        self.font = pygame.font.Font("assets/font.ttf", 12)
        self.icon_font = pygame.font.SysFont("segoeuisymbol", 24)
        
        # Simulation speed:
        self.step_size = 20
        self.min_step_size = 0
        self.max_step_size = 500  
        
        # Toolbox
        self.slow_down_button_rect = pygame.Rect(GRID_WIDTH_PX + 10, WINDOW_SIZE[1] - 50, 100, 40)
        self.pause_button_rect = pygame.Rect(GRID_WIDTH_PX + 110, WINDOW_SIZE[1] - 50, 100, 40)
        self.speed_up_button_rect = pygame.Rect(GRID_WIDTH_PX + 210, WINDOW_SIZE[1] - 50, 100, 40)
        self.clear_button_rect = pygame.Rect(GRID_WIDTH_PX + 400, WINDOW_SIZE[1] - 50, 40, 40)
        
        # Creation box
        self.draw_creation_box()
        

    def run(self):
        while self.running:
            delta_time = self.clock.tick(self.speed) / 1000
            
            self.handle_events()

            self.screen.fill(BLACK)

            # Draw the grid on 70% of the screen
            self.draw_grid()
            
            self.draw_leaderboard()

            self.draw_toolbox()

            if self.game_over:
                self.draw_game_over()

            self.manager.update(delta_time)
            self.manager.draw_ui(self.screen)
            
            pygame.display.update()

        self.quit_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.clear_button_rect.collidepoint(event.pos):
                    self.reset_game()
                elif self.pause_button_rect.collidepoint(event.pos):
                    self.paused = not self.paused
                elif self.speed_up_button_rect.collidepoint(event.pos):
                    self.step_size = min(self.step_size + ADD_STEP, self.max_step_size)  # Increase step size
                elif self.slow_down_button_rect.collidepoint(event.pos):
                    self.step_size = max(self.step_size - ADD_STEP, self.min_step_size)  # Decrease step size
                elif event.pos[0] < GRID_WIDTH_PX and not self.game_over:
                    grid_x = event.pos[0] // CELL_SIZE
                    grid_y = event.pos[1] // CELL_SIZE
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        self.add(grid_x, grid_y)
                        
            if event.type == gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.object_dropdown:
                    self.creation_selection = event.text
                elif event.ui_element == self.border_dropdown:
                    self.grid.change_border_type(BORDER_TYPES[event.text](self.grid.width, self.grid.height))
            
            if event.type == gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == self.pattern_input:
                    if event.text and all(c in 'LR' for c in event.text):
                        self.pattern_text = event.text
                elif event.ui_element == self.name_input:
                    self.machine_name = event.text
                elif event.ui_element == self.time_step_input:
                    if (event.text).isnumeric() and int(event.text) <= self.max_step_size and int(event.text) >= self.min_step_size:
                        self.step_size = int(event.text)
                        
            if event.type == gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.match_color_button:
                    # Generate colors
                    self.color_engine.generate_colors(len(self.pattern_text))
                    
            self.manager.process_events(event)

    def add(self, grid_x, grid_y):
        select = MACHINE_TYPES[self.creation_selection]
        if select[0] == "machine":
            self.machines.append(select[1](Coordinate(grid_x, grid_y), self.grid, name=self.machine_name, 
                                           pattern=self.pattern_text, colors=list(self.color_engine.generated_colors)))
        elif select[0] == "cell":
            pass
        
    def end_game(self):
        self.game_over = True

    def reset_game(self):
        # Reset the game state and clear the board
        self.grid = BaseGrid(GRID_WIDTH, GRID_HEIGHT, self.grid.border)  # Clear the grid
        self.machines = []  # Remove all machines
        self.game_over = False

    def quit_game(self):
        pygame.quit()

    #### UI stuff ###
    
    def draw_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                cell = self.grid.get_cell(x, y)
                pygame.draw.rect(self.screen, cell.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BORDER_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        if not self.paused and not self.game_over:
            # Execute multiple steps based on step_size
            for _ in range(self.step_size):
                for machine in self.machines:
                    machine.move()
                    if self.grid.check_border(machine):
                        self.end_game()
                        self.end_machine = machine
                        return

    def draw_leaderboard(self):
        pygame.draw.rect(self.screen, (50, 50, 50), (GRID_WIDTH_PX, 0, SIDEBAR_WIDTH, WINDOW_SIZE[1] / 4))
        
        leaderboard = sorted(self.machines, key=lambda m: m.score, reverse=True)[:5]
        title = self.font.render(f'Top 5 of {len(self.machines)}', True, (255, 0, 0))
        self.screen.blit(title, (GRID_WIDTH_PX + 10, 10))
        # Display the leaderboard entries
        for i, machine in enumerate(leaderboard):
            score_text = self.font.render(f"{machine.name}: {machine.score}", True, WHITE)
            self.screen.blit(score_text, (GRID_WIDTH_PX + 10, 40 + i * 25))

    def draw_game_over(self):
        # Display game over message in the middle of the grid
        top = sorted(self.machines, key=lambda m: m.score, reverse=True)[0]
        game_over_text = self.font.render(f"Game Over! {self.end_machine.name} hit the border. Machine {top.name} won !", True, BLUE)
        text_rect = game_over_text.get_rect(center=(GRID_WIDTH_PX // 2, WINDOW_SIZE[1] // 2))
        self.screen.blit(game_over_text, text_rect)

    def draw_toolbox(self):
        pygame.draw.rect(self.screen, (100, 50, 50), (GRID_WIDTH_PX, WINDOW_SIZE[1] - WINDOW_SIZE[1] / 10, SIDEBAR_WIDTH, WINDOW_SIZE[1] / 10))
        
        # Draw pause/resume button
        pygame.draw.rect(self.screen, (100, 100, 255), self.pause_button_rect)
        pause_symbol = "⏸" if not self.paused else "▶"
        pause_text = self.icon_font.render(pause_symbol, True, WHITE)
        pause_text_rect = pause_text.get_rect(center=self.pause_button_rect.center)
        self.screen.blit(pause_text, pause_text_rect)

        # Draw speed up button
        pygame.draw.rect(self.screen, (100, 255, 100), self.speed_up_button_rect)
        speed_up_symbol = "⏩"
        speed_up_text = self.icon_font.render(speed_up_symbol, True, WHITE)
        speed_up_text_rect = speed_up_text.get_rect(center=self.speed_up_button_rect.center)
        self.screen.blit(speed_up_text, speed_up_text_rect)

        # Draw slow down button
        pygame.draw.rect(self.screen, (255, 100, 100), self.slow_down_button_rect)
        slow_down_symbol = "⏪"
        slow_down_text = self.icon_font.render(slow_down_symbol, True, WHITE)
        slow_down_text_rect = slow_down_text.get_rect(center=self.slow_down_button_rect.center)
        self.screen.blit(slow_down_text, slow_down_text_rect)

        # Draw clear button (reload symbol)
        pygame.draw.rect(self.screen, CLEAR_BUTTON_COLOR, self.clear_button_rect)
        clear_symbol = "⟳"
        clear_text = self.icon_font.render(clear_symbol, True, WHITE)
        clear_text_rect = clear_text.get_rect(center=self.clear_button_rect.center)
        self.screen.blit(clear_text, clear_text_rect)

    def draw_creation_box(self):
        self.creation_selection = list(MACHINE_TYPES.keys())[0]
        self.object_dropdown = gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(GRID_WIDTH_PX + 10, 
                                                                                     WINDOW_SIZE[1] / 4 + 2,
                                                                                     WINDOW_SIZE[0] - GRID_WIDTH_PX - 150, 40), 
                                                           options_list=list(MACHINE_TYPES.keys()),
                                                           starting_option=list(MACHINE_TYPES.keys())[0],
                                                           manager=self.manager)
        
        self.border_type = "Periodic"
        self.border_dropdown = gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(GRID_WIDTH_PX + 10 + WINDOW_SIZE[0] - GRID_WIDTH_PX - 150 + 10, 
                                                                                     WINDOW_SIZE[1] / 4 + 2,
                                                                                     110, 40), 
                                                           options_list=list(BORDER_TYPES.keys()),
                                                           starting_option=list(BORDER_TYPES.keys())[0],
                                                           manager=self.manager)        

        self.pattern_text = "LR"
        self.pattern_input = gui.elements.UITextEntryLine(relative_rect=pygame.Rect(GRID_WIDTH_PX + 10, 
                                                                                     WINDOW_SIZE[1] / 4 + 50,
                                                                                     WINDOW_SIZE[0] - GRID_WIDTH_PX - 150, 40),
                                                    placeholder_text="Behavior/Pattern",
                                                    manager=self.manager)
        
        self.match_color_button = gui.elements.UIButton(relative_rect=pygame.Rect(GRID_WIDTH_PX + 320, 
                                                                                     WINDOW_SIZE[1] / 4 + 50,
                                                                                     110, 40),
                                                 text="Match to color", manager=self.manager)
        
        self.machine_name = f"Machine {len(self.machines)}"
        self.name_input = gui.elements.UITextEntryLine(relative_rect=pygame.Rect(GRID_WIDTH_PX + 10, 
                                                                                     WINDOW_SIZE[1] / 4 + 100,
                                                                                     WINDOW_SIZE[0] - GRID_WIDTH_PX - 30, 40),
                                                    placeholder_text="Machine name",
                                                    manager=self.manager)
        
        self.time_step_input = gui.elements.UITextEntryLine(relative_rect=pygame.Rect(GRID_WIDTH_PX + 320, 
                                                                                     WINDOW_SIZE[1] - 50,
                                                                                     70, 40),
                                                    placeholder_text="Step",
                                                    manager=self.manager)