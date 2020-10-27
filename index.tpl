<!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="Description" content="Web frontend for youtube-dl">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
    integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
  <link href="static/style.css" rel="stylesheet">

  <title>youtube-dl</title>
</head>

<body>
  <div class="container d-flex flex-column text-light">
    <div class="flex-grow-1"></div>
    <div class="jumbotron bg-transparent flex-grow-1 text-center">
      <h1 class="display-4">youtube-dl</h1>
      <p class="lead">Enter a video url to download the video to the server. Url can be to YouTube or <a
          class="text-info" href="https://rg3.github.io/youtube-dl/supportedsites.html">any
          other supported site</a>. The server will automatically download the highest quality version available.</p>
      <hr class="my-4">
      <div>
        <form action="/" method="POST">
          <div class="input-group">
            <input name="url" type="url" class="form-control" placeholder="URL" aria-label="URL"
              aria-describedby="button-submit" autofocus>
            <select class="custom-select" name="format">
              <optgroup label="Video">
                <option value="bestvideo">Best Video</option>
                <option value="mp4">MP4</option>
                <option value="flv">Flash Video (FLV)</option>
                <option value="webm">WebM</option>
                <option value="ogg">Ogg</option>
                <option value="mkv">Matroska (MKV)</option>
                <option value="avi">AVI</option>
              </optgroup>
              <optgroup label="Audio">
                <option value="bestaudio">Best Audio</option>
                <option value="aac">AAC</option>
                <option value="flac">FLAC</option>
                <option value="mp3">MP3</option>
                <option value="m4a">M4A</option>
                <option value="opus">Opus</option>
                <option value="vorbis">Vorbis</option>
                <option value="wav">WAV</option>
              </optgroup>
            </select>
            <div class="input-group-append">
              <button class="btn btn-primary" type="submit" id="button-submit">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    % if len(downloads):
    <h2>Downloads</h2>
    <table class="table">
      <thead>
        <th>#</th>
        <th>File name</th>
        <th>File size</th>
        <th>Progress</th>
        <th>Download speed</th>
      </thead>
      <tbody>
        % for download in downloads:
        <tr>
          <td>{{ download['id'] }}</td>
          <td>{{ download['filename'] }}</td>
          <td>{{ download['filesize'] }}</td>
          <td>{{ download['progress'] }}</td>
          <td>{{ download['speed'] }}</td>
        </tr>
        % end
      </tbody>
    </table>
    % end

    <footer>
      <div>
        <p class="text-muted">Web frontend for <a class="text-light"
            href="https://rg3.github.io/youtube-dl/">youtube-dl</a>,
          by <a class="text-light" href="https://twitter.com/manbearwiz">@manbearwiz</a>.</p>
      </div>
    </footer>
  </div>

</body>

</html>