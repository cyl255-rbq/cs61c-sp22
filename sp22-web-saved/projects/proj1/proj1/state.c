#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "snake_utils.h"
#include "state.h"

/* Helper function definitions */
static char get_board_at(game_state_t* state, int x, int y);
static void set_board_at(game_state_t* state, int x, int y, char ch);
static bool is_tail(char c);
static bool is_snake(char c);
static char body_to_tail(char c);
static int incr_x(char c);
static int incr_y(char c);
static void find_head(game_state_t* state, int snum);
static char next_square(game_state_t* state, int snum);
static void update_tail(game_state_t* state, int snum);
static void update_head(game_state_t* state, int snum);

/* Helper function to get a character from the board (already implemented for you). */
static char get_board_at(game_state_t* state, int x, int y) {
  return state->board[y][x];
}

/* Helper function to set a character on the board (already implemented for you). */
static void set_board_at(game_state_t* state, int x, int y, char ch) {
  state->board[y][x] = ch;
}

/* Task 1 */
game_state_t* create_default_state() {
  // TODO: Implement this function.
  game_state_t* game = (game_state_t*) malloc(sizeof(game_state_t));
  if (game == NULL)
  {
    return NULL;
  }
  game->x_size = 14;
  game->y_size = 10;
  game->num_snakes = 1;
  game->snakes = (snake_t*) malloc(sizeof(snake_t) * game->num_snakes);
  if (game->snakes == NULL)
  {
    free(game);
    return NULL;
  }
  game->snakes[0].head_x = 5;
  game->snakes[0].head_y = 4;
  game->snakes[0].tail_x = 4;
  game->snakes[0].tail_y = 4;
  game->snakes[0].live = true;
  game->board = (char**) malloc(sizeof(char*) * game->y_size);
  if (game->board == NULL) {
      free(game->snakes);
      free(game);
      return NULL;
  }
  for (unsigned int i = 0; i < game->y_size; i++) {
    game->board[i] = (char*) malloc(sizeof(char) * (game->x_size + 1));
    if (game->board[i] == NULL)
    {
      for (unsigned int j = 0; j < i; j++)
      {
        free(game->board[j]);
      }
      free(game->board);
      free(game->snakes);
      free(game);
      return NULL;
    }
  }
  for (unsigned int i = 0; i < game->y_size; i++)
  {
    for (unsigned int j = 0; j < game->x_size; j++)
    {
      if (i == 0 || i == (game->y_size - 1) || j == 0 || j == (game->x_size - 1))
      {
        game->board[i][j] = '#';
      } else {
        game->board[i][j] = ' ';
      }
    }
    game->board[i][game->x_size] = '\0';
  }
  game->board[4][4] = 'd';
  game->board[4][5] = '>';
  game->board[2][9] = '*';
  return game;
}

/* Task 2 */
void free_state(game_state_t* state) {
  // TODO: Implement this function.
  for (unsigned int i = 0; i < state->y_size; i++) {
    free(state->board[i]);
  }
  free(state->board);
  free(state->snakes);
  free(state);
  return;
}

/* Task 3 */
void print_board(game_state_t* state, FILE* fp) {
  // TODO: Implement this function.
  for (unsigned int i = 0; i < state->y_size; i++)
  {
    fprintf(fp, "%s\n", state->board[i]);
  }
  return;
}

/* Saves the current state into filename (already implemented for you). */
void save_board(game_state_t* state, char* filename) {
  FILE* f = fopen(filename, "w");
  print_board(state, f);
  fclose(f);
}

/* Task 4.1 */
static bool is_tail(char c) {
  // TODO: Implement this function.
  if (strchr("wasd", c))
  {
    return true;
  }
  return false;
}

static bool is_snake(char c) {
  // TODO: Implement this function.
  if (strchr("wasd^<>vx", c))
  {
    return true;
  }
  return false;
}

static char body_to_tail(char c) {
  // TODO: Implement this function.
  switch (c)
  {
  case '^':
    return 'w';
  case '<':
    return 'a';
  case '>':
    return 'd';
  case 'v':
    return 's';
  default:
    return c;
  }
}

static int incr_x(char c) {
  // TODO: Implement this function.
  if (strchr(">d", c))
  {
    return 1;
  } else if (strchr("<a", c))
  {
    return -1;
  }
  return 0;
}

static int incr_y(char c) {
  // TODO: Implement this function.
  if (strchr("vs", c))
  {
    return 1;
  } else if (strchr("^w", c))
  {
    return -1;
  }
  return 0;
}

/* Task 4.2 */
static char next_square(game_state_t* state, int snum) {
  // TODO: Implement this function.
  unsigned int cur_x = state->snakes[snum].head_x;
  unsigned int cur_y = state->snakes[snum].head_y;
  char head_char = get_board_at(state, cur_x, cur_y);
  unsigned int next_x = cur_x + incr_x(head_char);
  unsigned int next_y = cur_y + incr_y(head_char);
  return get_board_at(state, next_x, next_y);
}

/* Task 4.3 */
static void update_head(game_state_t* state, int snum) {
  // TODO: Implement this function.
  unsigned int cur_x = state->snakes[snum].head_x;
  unsigned int cur_y = state->snakes[snum].head_y;
  char head_char = get_board_at(state, cur_x, cur_y);
  unsigned int next_x = cur_x + incr_x(head_char);
  unsigned int next_y = cur_y + incr_y(head_char);
  set_board_at(state, next_x, next_y, head_char);
  state->snakes[snum].head_x = next_x;
  state->snakes[snum].head_y = next_y;
  return;
}

/* Task 4.4 */
static void update_tail(game_state_t* state, int snum) {
  // TODO: Implement this function.
  unsigned int cur_x = state->snakes[snum].tail_x;
  unsigned int cur_y = state->snakes[snum].tail_y;
  char cur_tail = get_board_at(state, cur_x, cur_y);
  unsigned int next_x = cur_x + incr_x(cur_tail);
  unsigned int next_y = cur_y + incr_y(cur_tail);
  char next_tail = get_board_at(state, next_x, next_y);
  set_board_at(state, cur_x, cur_y, ' ');
  set_board_at(state, next_x, next_y, body_to_tail(next_tail));
  state->snakes[snum].tail_x = next_x;
  state->snakes[snum].tail_y = next_y;
  return;
}

/* Task 4.5 */
void update_state(game_state_t* state, int (*add_food)(game_state_t* state)) {
  // TODO: Implement this function.
  for (unsigned int i = 0; i < state->num_snakes; i++)
  {
    snake_t* cur_snake = state->snakes + i;
    if (cur_snake->live == false) {
      continue;
    }
    char next = next_square(state, i);
    if (strchr("wasd^<v>#x", next))
    {
      cur_snake->live = false;
      set_board_at(state, cur_snake->head_x,  cur_snake->head_y, 'x');
    } else {
      update_head(state, i);
      if (next == '*')
      {
        add_food(state);
        continue;
      }  
      update_tail(state, i);
    }
  }
  return;
}

/* Task 5 */
game_state_t* load_board(char* filename) {
  // TODO: Implement this function.
  FILE* fp = fopen(filename, "r");
  if (fp == NULL)
  {
    return NULL;
  }
  unsigned int col = 0;
  unsigned int row = 0;
  char ch;
  while ((ch = fgetc(fp)) != '\n' && ch != EOF)
  {
    col++;
  }
  rewind(fp);
  char last_ch = '\n';
  while ((ch = fgetc(fp)) != EOF) {
    if (ch == '\n') {
      row++;
    }
    last_ch = ch;
  }
  if (last_ch != '\n') {//这里的目的是为了检查最后一个字符是不是\n，如果最后没有换行符但是结束了的话，可能导致row少+1
      row++;
  }
  game_state_t* game = (game_state_t*) malloc(sizeof(game_state_t));
  if (game == NULL)
  {
    fclose(fp);
    return NULL;
  }
  game->x_size = col;
  game->y_size = row;
  game->board = (char**) malloc(sizeof(char*) * row);
  if (game->board == NULL)
  {
    fclose(fp);
    free(game);
    return NULL;
  }
  for (unsigned int i = 0; i < row; i++)
  {
    game->board[i] = (char*) malloc(sizeof(char) * row + 1);
    if (game->board[i] == NULL)
    {
      fclose(fp);
      for (unsigned int j = 0; j < i; j++)
      {
        free(game->board[i]);
      }
      free(game->board);
      free(game->snakes);
      free(game);
      return NULL;
    }
  }
  rewind(fp);
  for (unsigned int i = 0; i < row; i++)
  {
    fgets(game->board[i], col + 1, fp);
    char scrap;
    while ((scrap = fgetc(fp)) != '\n' && scrap != EOF);//fgetc(fp);
  }
  fclose(fp);
  return game;
}

/* Task 6.1 */
static void find_head(game_state_t* state, int snum) {
  // TODO: Implement this function.
  unsigned int x = state->snakes[snum].tail_x;
  unsigned int y = state->snakes[snum].tail_y;
  char cur = get_board_at(state, x, y);
  while (strchr("^v<>x", get_board_at(state, x + incr_x(cur), y + incr_y(cur))))
  {
    x += incr_x(cur);
    y += incr_y(cur);
    cur = get_board_at(state, x, y);
  }
  state->snakes[snum].head_x = x;
  state->snakes[snum].head_y = y;
  return;
}

/* Task 6.2 */
game_state_t* initialize_snakes(game_state_t* state) {
  // TODO: Implement this function.
  state->snakes = NULL;
  state->num_snakes = 0;
  for (unsigned int i = 0; i < state->y_size; i++)
  {
    for (unsigned int j = 0; j < state->x_size; j++)
    {
      if (strchr("wasd", state->board[i][j]))
      {
        state->num_snakes++;
        snake_t* temp = realloc(state->snakes, sizeof(snake_t) * state->num_snakes);
        if (temp == NULL)
        {
          if (state->snakes != NULL)
          {
            free(state->snakes);
          }
          for (unsigned int k = 0; k < state->y_size; k++)
          {
            free(state->board[k]);
          }
          free(state->board);
          free(state);
          return NULL;
        }
        state->snakes = temp;
        snake_t* snake = &(state->snakes[state->num_snakes - 1]);
        snake->tail_x = j;
        snake->tail_y = i;
        snake->live = true;
        find_head(state, state->num_snakes - 1);
      }
    }
  }
  return state;
}
