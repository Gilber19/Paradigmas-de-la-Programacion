#include "raylib.h"
#include <stdlib.h>
#include <time.h>
#include <stdio.h>

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 600
#define GRID_SIZE 20

typedef enum
{
    UP,
    DOWN,
    LEFT,
    RIGHT
} Direction;

typedef struct Node
{
    int x;
    int y;
    struct Node *next;
} Node;

typedef struct
{
    Node *head;
    int length;
    Direction direction;
} Snake;

typedef struct
{
    int x;
    int y;
} Fruit;

Node *create_node(int x, int y)
{
    Node *new_node = (Node *)malloc(sizeof(Node));
    if (new_node != NULL)
    {
        new_node->x = x;
        new_node->y = y;
        new_node->next = NULL;
    }
    return new_node;
}

void append_node(Node **head, int x, int y)
{
    Node *new_node = create_node(x, y);
    if (*head == NULL)
    {
        *head = new_node;
    }
    else
    {
        Node *temp = *head;
        while (temp->next != NULL)
        {
            temp = temp->next;
        }
        temp->next = new_node;
    }
}

void free_list(Node *head)
{
    while (head != NULL)
    {
        Node *temp = head;
        head = head->next;
        free(temp);
    }
}

void init_game(Snake *snake, Fruit *fruit, int *snake_speed)
{
    snake->head = create_node(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2);
    snake->length = 1;
    snake->direction = RIGHT;

    fruit->x = (rand() % (SCREEN_WIDTH / GRID_SIZE)) * GRID_SIZE;
    fruit->y = (rand() % (SCREEN_HEIGHT / GRID_SIZE)) * GRID_SIZE;
    *snake_speed = 5;
}

void update_game(Snake *snake, Fruit *fruit, int *game_over, Sound eat_sound, Sound die_sound, int *snake_speed)
{
    static int frame_counter = 0;

    if (frame_counter >= 60 / *snake_speed)
    {
        Node *new_head = create_node(snake->head->x, snake->head->y);
        if (snake->direction == UP)
            new_head->y -= GRID_SIZE;
        if (snake->direction == DOWN)
            new_head->y += GRID_SIZE;
        if (snake->direction == LEFT)
            new_head->x -= GRID_SIZE;
        if (snake->direction == RIGHT)
            new_head->x += GRID_SIZE;

        new_head->next = snake->head;
        snake->head = new_head;
        snake->length++;

        if (new_head->x == fruit->x && new_head->y == fruit->y)
        {
            fruit->x = (rand() % (SCREEN_WIDTH / GRID_SIZE)) * GRID_SIZE;
            fruit->y = (rand() % (SCREEN_HEIGHT / GRID_SIZE)) * GRID_SIZE;
            *snake_speed = *snake_speed + (*snake_speed * 0.2f);
            PlaySound(eat_sound);
        }
        else
        {
            Node *temp = snake->head;
            for (int i = 0; i < snake->length - 1; i++)
            {
                temp = temp->next;
            }
            Node *tail = temp->next;
            temp->next = NULL;
            free(tail);
            snake->length--;
        }

        if (new_head->x < 0 || new_head->x >= SCREEN_WIDTH || new_head->y < 0 || new_head->y >= SCREEN_HEIGHT)
        {
            *game_over = 1;
            PlaySound(die_sound);
        }

        Node *current = new_head->next;
        while (current != NULL)
        {
            if (new_head->x == current->x && new_head->y == current->y)
            {
                *game_over = 1;
                PlaySound(die_sound);
            }
            current = current->next;
        }

        frame_counter = 0;
    }
    else
    {
        frame_counter++;
    }
}

void draw_game(Snake *snake, Fruit *fruit, Texture2D apple, Texture2D texture)
{
    DrawTexture(texture, 0, 0, RAYWHITE);
    bool is_red = true;

    Node *current = snake->head;
    while (current != NULL)
    {
        Color color = (is_red) ? RED : BLACK;
        DrawCircle(current->x + GRID_SIZE / 2, current->y + GRID_SIZE / 2, GRID_SIZE / 2, color);
        is_red = !is_red;
        current = current->next;
    }

    DrawTexturePro(apple, (Rectangle){0, 0, apple.width, apple.height}, (Rectangle){fruit->x, fruit->y, 20, 20}, (Vector2){0, 0}, 0.0f, RAYWHITE);
}

int main(void)
{
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake Game");
    InitAudioDevice();

    Snake snake;
    Fruit fruit;
    int game_over = 0;
    int snake_speed = 5;
    int is_paused = 0;

    srand(time(NULL));

    Sound eat_sound = LoadSound("mordida.wav");
    Sound die_sound = LoadSound("over.wav");
    Music background_music = LoadMusicStream("musica.wav");

    PlayMusicStream(background_music);
    SetMusicVolume(background_music, 0.2f);

    init_game(&snake, &fruit, &snake_speed);

    Texture2D texture = LoadTexture("newfondo.png");
    Texture2D apple = LoadTexture("manzana.png");

    SetTargetFPS(60);

    while (!WindowShouldClose())
    {
        UpdateMusicStream(background_music);

        if (IsKeyPressed(KEY_P))
        {
            is_paused = !is_paused;
        }

        if (!is_paused && !game_over)
        {
            if (IsKeyPressed(KEY_UP) && snake.direction != DOWN)
                snake.direction = UP;
            if (IsKeyPressed(KEY_DOWN) && snake.direction != UP)
                snake.direction = DOWN;
            if (IsKeyPressed(KEY_LEFT) && snake.direction != RIGHT)
                snake.direction = LEFT;
            if (IsKeyPressed(KEY_RIGHT) && snake.direction != LEFT)
                snake.direction = RIGHT;

            update_game(&snake, &fruit, &game_over, eat_sound, die_sound, &snake_speed);
        }

        BeginDrawing();
        ClearBackground(RAYWHITE);

        if (!is_paused)
        {
            draw_game(&snake, &fruit, apple, texture);
            if (game_over)
            {
                DrawText("GAME OVER", SCREEN_WIDTH / 2 - MeasureText("GAME OVER", 20) / 2, SCREEN_HEIGHT / 2 - 10, 20, RED);
                DrawText("Press [R] to Restart", SCREEN_WIDTH / 2 - MeasureText("Press [R] to Restart", 20) / 2, SCREEN_HEIGHT / 2 + 20, 20, GRAY);
                if (IsKeyPressed(KEY_R))
                {
                    free_list(snake.head);
                    init_game(&snake, &fruit, &snake_speed);
                    game_over = 0;
                }
            }
        }
        else
        {
            DrawText("PAUSE", SCREEN_WIDTH / 2 - MeasureText("PAUSE", 20) / 2, SCREEN_HEIGHT / 2 - 10, 20, BLACK);
        }

        EndDrawing();
    }

    free_list(snake.head);
    UnloadTexture(texture);
    UnloadTexture(apple);
    UnloadSound(eat_sound);
    UnloadSound(die_sound);
    UnloadMusicStream(background_music);
    CloseAudioDevice();
    CloseWindow();

    return 0;
}
